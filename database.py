import sqlite3
from typing import List, Optional, Dict, Any

# Connect to the database
def connect_db(db_name: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
    return conn

# Create tables from the SQL schema
def create_tables(db_name: str, schema_file: str):
    conn = connect_db(db_name)
    with open(schema_file, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

# Basic CRUD operations for the `victims` table
def add_victim(db_name: str, name: str, email: str, phone: Optional[str], country: str, region: Optional[str]):
    conn = connect_db(db_name)
    conn.execute("""
        INSERT INTO victims (name, email, phone, country, region) 
        VALUES (?, ?, ?, ?, ?)""", (name, email, phone, country, region))
    conn.commit()
    conn.close()

def update_victim_status(db_name: str, victim_id: int, completed: bool):
    conn = connect_db(db_name)
    conn.execute("UPDATE victims SET completed = ? WHERE id = ?", (completed, victim_id))
    conn.commit()
    conn.close()

def get_all_victims(db_name: str) -> List[Dict[str, Any]]:
    conn = connect_db(db_name)
    cursor = conn.execute("SELECT * FROM victims")
    victims = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return victims

# CRUD operations for `resources` table
def add_resource(db_name: str, victim_id: int, resource_type: str, description: Optional[str]):
    conn = connect_db(db_name)
    conn.execute("""
        INSERT INTO resources (victim_id, resource_type, description) 
        VALUES (?, ?, ?)""", (victim_id, resource_type, description))
    conn.commit()
    conn.close()

def update_resource_status(db_name: str, resource_id: int, completed: bool):
    conn = connect_db(db_name)
    conn.execute("UPDATE resources SET completed = ? WHERE id = ?", (completed, resource_id))
    conn.commit()
    conn.close()

# CRUD operations for `donors` table
def add_donor(db_name: str, name: str, email: str, phone: Optional[str], country: str, region: Optional[str]):
    conn = connect_db(db_name)
    conn.execute("""
        INSERT INTO donors (name, email, phone, country, region) 
        VALUES (?, ?, ?, ?, ?)""", (name, email, phone, country, region))
    conn.commit()
    conn.close()

def update_donor_status(db_name: str, donor_id: int, completed: bool):
    conn = connect_db(db_name)
    conn.execute("UPDATE donors SET completed = ? WHERE id = ?", (completed, donor_id))
    conn.commit()
    conn.close()

# CRUD operations for `donor_resources` table
def add_donor_resource(db_name: str, donor_id: int, resource_type: str, description: Optional[str]):
    conn = connect_db(db_name)
    conn.execute("""
        INSERT INTO donor_resources (donor_id, resource_type, description) 
        VALUES (?, ?, ?)""", (donor_id, resource_type, description))
    conn.commit()
    conn.close()

def update_donor_resource_status(db_name: str, donor_resource_id: int, completed: bool):
    conn = connect_db(db_name)
    conn.execute("UPDATE donor_resources SET completed = ? WHERE id = ?", (completed, donor_resource_id))
    conn.commit()
    conn.close()

# Matching resources with donor resources
def add_match(db_name: str, resource_id: int, donor_resource_id: int):
    conn = connect_db(db_name)
    conn.execute("""
        INSERT INTO matches (resource_id, donor_resource_id) 
        VALUES (?, ?)""", (resource_id, donor_resource_id))
    conn.commit()
    conn.close()

# Retrieve all matches
def get_all_matches(db_name: str) -> List[Dict[str, Any]]:
    conn = connect_db(db_name)
    cursor = conn.execute("SELECT * FROM matches")
    matches = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return matches

# Utility to close database connection
def close_db(conn: sqlite3.Connection):
    conn.close()
