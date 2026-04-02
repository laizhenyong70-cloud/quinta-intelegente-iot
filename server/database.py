import sqlite3
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents= True ,exist_ok=True)
    conn: sqlite3.Connection = sqlite3.connect(str(DB_PATH))
    return conn


def init_db() -> None:
    
    conn = get_connection()
    cursor = conn.cursor()
    
    
    cursor.execute(
     """
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            nh3 REAL NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

def insert_sensor_data(
      sensor_id:str,
      temperature:float,
      humidity:float,
      nh3:float,
      status:str,
      timestamp:str,
) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO sensor_data (
            sensor_id, temperature, humidity, nh3, status, timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (sensor_id, temperature, humidity, nh3, status, timestamp),
    )
    conn.commit()
    conn.close()
def get_latest_data():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT id, temperature, humidity, nh3, status, timestamp
        FROM sensor_data
        ORDER BY timestamp DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id":row[0],
            "temperature":row[1],
            "humidity":row[2],
            "nh3":row[3],
            "status":row[4],
            "timestamp":row[5]
        }

    return None

def get_history_data(limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, temperature, humidity, nh3, status, timestamp
        FROM sensor_data
        ORDER BY timestamp DESC
        LIMIT ?
    """,(limit,))
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id":row[0],
            "temperature":row[1],
            "humidity":row[2],
            "nh3":row[3],
            "status":row[4],
            "timestamp":row[5]
        })
    return result
    
    