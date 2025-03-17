import random
import pandas as pd
from datetime import datetime, timedelta

def generate_aircraft_data():
    aircraft_types = ['F-22', 'F-35', 'F-16', 'C-130', 'KC-135']
    
    data = {
        'aircraft_id': [f'AC{i:03d}' for i in range(10)],
        'type': [random.choice(aircraft_types) for _ in range(10)],
        'latitude': [random.uniform(25, 49) for _ in range(10)],
        'longitude': [random.uniform(-125, -70) for _ in range(10)],
        'altitude': [random.uniform(25000, 45000) for _ in range(10)],
        'speed': [random.uniform(400, 1200) for _ in range(10)],
        'heading': [random.uniform(0, 360) for _ in range(10)]
    }
    return pd.DataFrame(data)

def generate_inventory_data():
    items = ['Engine Parts', 'Avionics', 'Landing Gear', 'Fuel Tanks', 'Weapons Systems']
    
    data = {
        'item_id': [f'INV{i:03d}' for i in range(20)],
        'item_name': [random.choice(items) for _ in range(20)],
        'quantity': [random.randint(1, 100) for _ in range(20)],
        'status': [random.choice(['Available', 'In Use', 'Maintenance']) for _ in range(20)],
        'last_updated': [(datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d') for _ in range(20)]
    }
    return pd.DataFrame(data)

def generate_comm_logs():
    message_types = ['Status Update', 'Mission Brief', 'Emergency Alert', 'Weather Report']
    
    data = {
        'timestamp': [(datetime.now() - timedelta(minutes=random.randint(0, 360))).strftime('%Y-%m-%d %H:%M:%S') for _ in range(15)],
        'message_type': [random.choice(message_types) for _ in range(15)],
        'priority': [random.choice(['High', 'Medium', 'Low']) for _ in range(15)],
        'message': [f'Communication log entry {i}' for i in range(15)],
        'status': [random.choice(['Received', 'Pending', 'Acknowledged']) for _ in range(15)]
    }
    return pd.DataFrame(data)
