import os
import psycopg2
import pandas as pd
from datetime import datetime
import json
import tempfile

class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('PGHOST'),
                database=os.getenv('PGDATABASE'),
                user=os.getenv('PGUSER'),
                password=os.getenv('PGPASSWORD'),
                port=os.getenv('PGPORT')
            )
            self.cursor = self.connection.cursor()
            self.using_fallback = False
            self.create_tables()
        except Exception as e:
            print(f"Database connection error: {e}")
            print("Using local file-based fallback database")
            self.using_fallback = True
            self.data_dir = os.path.join(tempfile.gettempdir(), 'aerospace_defense_data')
            os.makedirs(self.data_dir, exist_ok=True)
            
            # Initialize empty tables if they don't exist
            self._init_fallback_tables()

    def create_tables(self):
        # Aircraft tracking table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS aircraft (
                aircraft_id VARCHAR(10) PRIMARY KEY,
                type VARCHAR(50),
                latitude FLOAT,
                longitude FLOAT,
                altitude FLOAT,
                speed FLOAT,
                heading FLOAT,
                last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Inventory management table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                item_id VARCHAR(10) PRIMARY KEY,
                item_name VARCHAR(100),
                quantity INTEGER,
                status VARCHAR(50),
                last_updated DATE DEFAULT CURRENT_DATE
            )
        """)

        # Communications log table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS communications (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                message_type VARCHAR(50),
                priority VARCHAR(20),
                message TEXT,
                status VARCHAR(20)
            )
        """)
        
        # Users table for authentication
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(50) PRIMARY KEY,
                password_hash VARCHAR(64) NOT NULL
            )
        """)

        self.connection.commit()

    def insert_aircraft(self, aircraft_data):
        if self.using_fallback:
            aircraft = self._read_fallback_table('aircraft')
            aircraft_data['last_update'] = datetime.now().isoformat()
            aircraft[aircraft_data['aircraft_id']] = aircraft_data
            self._write_fallback_table('aircraft', aircraft)
        else:
            sql = """
                INSERT INTO aircraft (aircraft_id, type, latitude, longitude, altitude, speed, heading)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (aircraft_id) 
                DO UPDATE SET 
                    type = EXCLUDED.type,
                    latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude,
                    altitude = EXCLUDED.altitude,
                    speed = EXCLUDED.speed,
                    heading = EXCLUDED.heading,
                    last_update = CURRENT_TIMESTAMP
            """
            self.cursor.execute(sql, (
                aircraft_data['aircraft_id'],
                aircraft_data['type'],
                aircraft_data['latitude'],
                aircraft_data['longitude'],
                aircraft_data['altitude'],
                aircraft_data['speed'],
                aircraft_data['heading']
            ))
            self.connection.commit()

    def get_all_aircraft(self):
        if self.using_fallback:
            aircraft = self._read_fallback_table('aircraft')
            if not aircraft:
                return pd.DataFrame(columns=['aircraft_id', 'type', 'latitude', 'longitude', 'altitude', 'speed', 'heading', 'last_update'])
            return pd.DataFrame(list(aircraft.values()))
        else:
            self.cursor.execute("SELECT * FROM aircraft")
            columns = [desc[0] for desc in self.cursor.description]
            return pd.DataFrame(self.cursor.fetchall(), columns=columns)

    def insert_inventory_item(self, item_data):
        if self.using_fallback:
            inventory = self._read_fallback_table('inventory')
            item_data['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            inventory[item_data['item_id']] = item_data
            self._write_fallback_table('inventory', inventory)
        else:
            sql = """
                INSERT INTO inventory (item_id, item_name, quantity, status)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (item_id)
                DO UPDATE SET
                    item_name = EXCLUDED.item_name,
                    quantity = EXCLUDED.quantity,
                    status = EXCLUDED.status,
                    last_updated = CURRENT_DATE
            """
            self.cursor.execute(sql, (
                item_data['item_id'],
                item_data['item_name'],
                item_data['quantity'],
                item_data['status']
            ))
            self.connection.commit()

    def get_all_inventory(self):
        if self.using_fallback:
            inventory = self._read_fallback_table('inventory')
            if not inventory:
                return pd.DataFrame(columns=['item_id', 'item_name', 'quantity', 'status', 'last_updated'])
            return pd.DataFrame(list(inventory.values()))
        else:
            self.cursor.execute("SELECT * FROM inventory")
            columns = [desc[0] for desc in self.cursor.description]
            return pd.DataFrame(self.cursor.fetchall(), columns=columns)

    def log_communication(self, comm_data):
        if self.using_fallback:
            communications = self._read_fallback_table('communications')
            comm_data['timestamp'] = datetime.now().isoformat()
            comm_data['id'] = len(communications) + 1
            communications.append(comm_data)
            self._write_fallback_table('communications', communications)
            return comm_data['id']
        else:
            sql = """
                INSERT INTO communications (message_type, priority, message, status)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """
            self.cursor.execute(sql, (
                comm_data['message_type'],
                comm_data['priority'],
                comm_data['message'],
                comm_data['status']
            ))
            self.connection.commit()
            return self.cursor.fetchone()[0]

    def get_communications(self, limit=50):
        if self.using_fallback:
            communications = self._read_fallback_table('communications')
            if not communications:
                return pd.DataFrame(columns=['id', 'timestamp', 'message_type', 'priority', 'message', 'status'])
            # Sort by timestamp in descending order
            sorted_comms = sorted(communications, key=lambda x: x['timestamp'], reverse=True)
            return pd.DataFrame(sorted_comms[:limit])
        else:
            self.cursor.execute("SELECT * FROM communications ORDER BY timestamp DESC LIMIT %s", (limit,))
            columns = [desc[0] for desc in self.cursor.description]
            return pd.DataFrame(self.cursor.fetchall(), columns=columns)

    def _init_fallback_tables(self):
        """Initialize empty tables for fallback storage"""
        tables = {
            'aircraft': os.path.join(self.data_dir, 'aircraft.json'),
            'inventory': os.path.join(self.data_dir, 'inventory.json'),
            'communications': os.path.join(self.data_dir, 'communications.json'),
            'users': os.path.join(self.data_dir, 'users.json')
        }
        
        for table, path in tables.items():
            if not os.path.exists(path):
                if table == 'communications':
                    with open(path, 'w') as f:
                        json.dump([], f)
                else:
                    with open(path, 'w') as f:
                        json.dump({}, f)
    
    def _read_fallback_table(self, table_name):
        """Read data from fallback storage"""
        path = os.path.join(self.data_dir, f'{table_name}.json')
        with open(path, 'r') as f:
            return json.load(f)
    
    def _write_fallback_table(self, table_name, data):
        """Write data to fallback storage"""
        path = os.path.join(self.data_dir, f'{table_name}.json')
        with open(path, 'w') as f:
            json.dump(data, f)
    
    def close(self):
        if not self.using_fallback:
            self.cursor.close()
            self.connection.close()

    # User authentication methods for fallback
    def check_user_credentials(self, username, password_hash):
        if self.using_fallback:
            users = self._read_fallback_table('users')
            return username in users and users[username] == password_hash
        else:
            self.cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
            result = self.cursor.fetchone()
            return result and result[0] == password_hash
    
    def user_exists(self, username):
        if self.using_fallback:
            users = self._read_fallback_table('users')
            return username in users
        else:
            self.cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            return self.cursor.fetchone() is not None
    
    def add_user(self, username, password_hash):
        if self.using_fallback:
            users = self._read_fallback_table('users')
            users[username] = password_hash
            self._write_fallback_table('users', users)
        else:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash)
            )
            self.connection.commit()
