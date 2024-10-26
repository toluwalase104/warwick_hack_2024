import sqlite3

# Function to connect to the SQLite database and initialize it with schema.sql
def connect_and_initialize(db_path="database.db", schema_path="schema.sql"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Read schema from the file and execute it
    with open(schema_path, 'r') as f:
        schema = f.read()
    cursor.executescript(schema)
    conn.commit()
    return conn

# Function to add a new victim
def add_victim(conn, name, email, phone, postcode, address, country, completed=0, description=""):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO victims (name, email, phone, postcode, address, country, completed, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, email, phone, postcode, address, country, completed, description))
    conn.commit()
    return cursor.lastrowid  # Returns the ID of the inserted row

# Function to add a requested resource for a victim
def add_requested_resource(conn, victim_id, resource_type):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO requested_resources (victim_id, resource_type)
        VALUES (?, ?)
    """, (victim_id, resource_type))
    conn.commit()
    return cursor.lastrowid

# Function to add a new donor
def add_donor(conn, name, email, phone, postcode, address, country, completed=0, description=""):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO donors (name, email, phone, postcode, address, country, completed, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, email, phone, postcode, address, country, completed, description))
    conn.commit()
    return cursor.lastrowid

# Function to add a resource that a donor can provide
def add_donor_resource(conn, donor_id, resource_type):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO donor_resources (donor_id, resource_type)
        VALUES (?, ?)
    """, (donor_id, resource_type))
    conn.commit()
    return cursor.lastrowid

# Function to create a match between a requested resource and a donor's resource
def add_match(conn, resource_id, donor_resource_id):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO matches (resource_id, donor_resource_id)
        VALUES (?, ?)
    """, (resource_id, donor_resource_id))
    conn.commit()
    return cursor.lastrowid

# Function to retrieve all victims
def get_all_victims(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM victims")
    return cursor.fetchall()

# Function to retrieve all donors
def get_all_donors(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    return cursor.fetchall()

# Function to find all matches for a specific victim
def get_matches_for_victim(conn, victim_id):
    cursor = conn.cursor()
    query = """
        SELECT m.id, rr.resource_type, dr.resource_type
        FROM matches m
        JOIN requested_resources rr ON m.resource_id = rr.id
        JOIN donor_resources dr ON m.donor_resource_id = dr.id
        WHERE rr.victim_id = ?
    """
    cursor.execute(query, (victim_id,))
    return cursor.fetchall()

# Function to find all matches for a specific donor
def get_matches_for_donor(conn, donor_id):
    cursor = conn.cursor()
    query = """
        SELECT m.id, rr.resource_type AS requested_resource_type,
               dr.resource_type AS donor_resource_type
        FROM matches m
        JOIN requested_resources rr ON m.resource_id = rr.id
        JOIN donor_resources dr ON m.donor_resource_id = dr.id
        WHERE dr.donor_id = ?
    """
    cursor.execute(query, (donor_id,))
    return cursor.fetchall()

# Function to close the database connection
def close_connection(conn):
    conn.close()

if __name__ == "__main__":
    # Initialize and connect to the database
    conn = connect_and_initialize()

    # Add a victim
    victim_id = add_victim(conn, "John Doe", "john@example.com", "1234567890", "12345", "123 Main St", "USA")

    # Add a requested resource for the victim
    requested_resource_id = add_requested_resource(conn, victim_id, "Food")

    # Add a donor
    donor_id = add_donor(conn, "Jane Smith", "jane@example.com", "0987654321", "54321", "456 Elm St", "USA")

    # Add a resource that the donor can provide
    donor_resource_id = add_donor_resource(conn, donor_id, "Food")

    # Create a match between the requested resource and the donor's resource
    match_id = add_match(conn, requested_resource_id, donor_resource_id)

    # Retrieve and print all victims
    print("Victims:", get_all_victims(conn))

    # Retrieve and print all donors
    print("Donors:", get_all_donors(conn))

    # Retrieve and print matches for the victim
    print("Matches for victim:", get_matches_for_victim(conn, victim_id))

    # Retrieve and print matches for the donor
    print("Matches for donor:", get_matches_for_donor(conn, donor_id))

    # Close the connection
    close_connection(conn)
