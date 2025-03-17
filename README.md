# Aerospace Defense System

A comprehensive aerospace and defense web application that empowers teams with advanced inventory management, secure authentication, and real-time tracking capabilities. The application provides robust data export and reporting tools for enhanced operational insights.

## Features

- Aircraft tracking with interactive map visualization
- Inventory management
- Communications logging
- Data export and reporting
- User authentication

## Local Setup Instructions

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database (optional - falls back to file-based storage if unavailable)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd aerospace-defense-system
```

### Step 2: Create and Activate a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a requirements.txt file, install the following packages:

```bash
pip install folium mysql-connector-python openpyxl pandas plotly psycopg2-binary streamlit streamlit-folium twilio
```

### Step 4: Database Configuration (Optional)

The application will work without a database by using a fallback file-based storage system. However, for full functionality, configure the following environment variables to connect to your PostgreSQL database:

```bash
# On Windows
set PGHOST=your_host
set PGDATABASE=your_database
set PGUSER=your_username
set PGPASSWORD=your_password
set PGPORT=your_port

# On macOS/Linux
export PGHOST=your_host
export PGDATABASE=your_database
export PGUSER=your_username
export PGPASSWORD=your_password
export PGPORT=your_port
```

### Step 5: Create Configuration Directory

Create a `.streamlit` directory and config file:

```bash
mkdir -p .streamlit
```

Create a file `.streamlit/config.toml` with the following content:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501
```

### Step 6: Run the Application

```bash
streamlit run main.py
```

The application will be available at `http://localhost:8501` in your web browser.

## Usage

1. Login with your username and password. If running for the first time, you'll be prompted to create an account.
2. Navigate through the sidebar menu to access different features:
   - Dashboard: View aircraft tracking
   - Inventory: Manage inventory items
   - Communications: Log and view communications
   - Export & Reports: Generate and download reports

## Deployment

For deployment on platforms like Replit, the application is configured to run with the command:

```bash
streamlit run main.py --server.address 0.0.0.0 --server.port 8501
```

## Technologies Used

- Python 3.11
- Streamlit framework
- PostgreSQL database
- Plotly and Folium for geospatial visualization
- Openpyxl for data export
- Advanced user authentication and reporting system