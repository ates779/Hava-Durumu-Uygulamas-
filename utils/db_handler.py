import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'weather_history.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT NOT NULL,
            temp REAL,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_search(city_name, temp, description):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Check if city already exists to update or just insert new
    # Actually, let's keep history so we just insert.
    cursor.execute('''
        INSERT INTO history (city_name, temp, description)
        VALUES (?, ?, ?)
    ''', (city_name, temp, description))
    conn.commit()
    conn.close()

def get_recent_searches(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT city_name, temp, description, timestamp 
        FROM history 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    # Return unique cities, keeping the most recent
    seen = set()
    unique_rows = []
    for row in rows:
        city = row[0].lower()
        if city not in seen:
            seen.add(city)
            unique_rows.append(row)
            if len(unique_rows) >= 5: # Just keep 5 unique
                break
    return unique_rows
