import sqlite3
from collections import defaultdict

# Function to connect to the SQLite database and initialize it with schema.sql
def connect_and_initialize(db_path="database.db", schema_path="schema.sql"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Allows row access by column name

    cursor = conn.cursor()
    # Read schema from the file and execute it
    with open(schema_path, 'r') as f:
        schema = f.read()
    cursor.executescript(schema)
    conn.commit()
    return conn

# Function to add a new victim
def add_victim(conn, name, contact, postcode, address, country, description=""):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO victims (name, contact, postcode, address, country, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, contact, postcode, address, country, description))
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
def add_donor(conn, name, contact, postcode, address, country, description=""):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO donors (name, contact, postcode, address, country, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, contact, postcode, address, country, description))
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

def mark_as_matched(conn, victim_id, donor_id):
    cursor = conn.cursor()
    try:
        # Insert into matches table to mark as matched
        cursor.execute("""
            INSERT INTO matches (victim_id, donor_id)
            VALUES (?, ?)
        """, (victim_id, donor_id))
        conn.commit()
        
        # Retrieve the ID of the created match
        match_id = cursor.lastrowid

        # Update the `completed` status for both the victim and the donor
        cursor.execute("UPDATE victims SET completed = 1 WHERE id = ?", (victim_id,))
        cursor.execute("UPDATE donors SET completed = 1 WHERE id = ?", (donor_id,))
        conn.commit()

        return match_id
    
    except sqlite3.IntegrityError as e:
        print("Error marking as matched:", e)
        return None

def get_unmatched_victims_with_resources(conn):
    cursor = conn.cursor()
    query = """
        SELECT victims.id, victims.name, victims.contact, victims.country, requested_resources.resource_type
        FROM victims
        JOIN requested_resources ON victims.id = requested_resources.victim_id
        WHERE victims.completed = 0
    """
    cursor.execute(query)
    
    # Use a defaultdict to accumulate resources for each victim
    victim_dict = defaultdict(lambda: {"id": None, "name": "", "contact": "", "country": "", "resources": []})
    
    for row in cursor.fetchall():
        victim_id = row["id"]
        victim_dict[victim_id]["id"] = victim_id
        victim_dict[victim_id]["name"] = row["name"]
        victim_dict[victim_id]["contact"] = row["contact"]
        victim_dict[victim_id]["country"] = row["country"]
        victim_dict[victim_id]["resources"].append(row["resource_type"])

    # Convert the dictionary to a list of dictionaries
    return list(victim_dict.values())

def get_unmatched_donors_with_resources(conn):
    cursor = conn.cursor()
    query = """
        SELECT donors.id, donors.name, donors.contact, donors.country, donor_resources.resource_type
        FROM donors
        JOIN donor_resources ON donors.id = donor_resources.donor_id
        WHERE donors.completed = 0
    """
    cursor.execute(query)
    
    # Use a defaultdict to accumulate resources for each donor
    donor_dict = defaultdict(lambda: {"id": None, "name": "", "contact": "", "country": "", "resources": []})
    
    for row in cursor.fetchall():
        donor_id = row["id"]
        donor_dict[donor_id]["id"] = donor_id
        donor_dict[donor_id]["name"] = row["name"]
        donor_dict[donor_id]["contact"] = row["contact"]
        donor_dict[donor_id]["country"] = row["country"]
        donor_dict[donor_id]["resources"].append(row["resource_type"])

    # Convert the dictionary to a list of dictionaries
    return list(donor_dict.values())

def is_victim_matched(conn, victim_id):
    """
    Checks if a victim has been matched by examining their `completed` status.

    Parameters:
    - conn: SQLite database connection
    - victim_id: The ID of the victim to check

    Returns:
    - True if the victim has been matched (completed = 1), False otherwise
    """
    cursor = conn.cursor()
    cursor.execute("SELECT completed FROM victims WHERE id = ?", (victim_id,))
    result = cursor.fetchone()
    return result is not None and result[0] == 1

def is_donor_matched(conn, donor_id):
    """
    Checks if a donor has been matched by examining their `completed` status.

    Parameters:
    - conn: SQLite database connection
    - donor_id: The ID of the donor to check

    Returns:
    - True if the donor has been matched (completed = 1), False otherwise
    """
    cursor = conn.cursor()
    cursor.execute("SELECT completed FROM donors WHERE id = ?", (donor_id,))
    result = cursor.fetchone()
    return result is not None and result[0] == 1

# Function to close the database connection
def close_connection(conn):
    conn.close()

if __name__ == "__main__":
    # Initialize and connect to the database
    conn = connect_and_initialize()

    # 1. Add victims and requested resources
    print("Adding victims and their requested resources:")
    victim_id1 = add_victim(conn, "John Doe", "john@example.com", "12345", "123 Main St", "USA", "Needs food and shelter")
    add_requested_resource(conn, victim_id1, "Food")
    add_requested_resource(conn, victim_id1, "Shelter")
    print(f"Added victim John Doe with ID: {victim_id1}")

    victim_id2 = add_victim(conn, "Alice Brown", "alice@example.com", "10001", "789 Maple St", "USA", "Needs food and clothes")
    add_requested_resource(conn, victim_id2, "Food")
    add_requested_resource(conn, victim_id2, "Clothes")
    print(f"Added victim Alice Brown with ID: {victim_id2}\n")

    # 2. Add donors and their available resources
    print("Adding donors and their available resources:")
    donor_id1 = add_donor(conn, "Bob White", "bob@example.com", "10002", "101 Pine St", "USA", "Can provide food and clothes")
    add_donor_resource(conn, donor_id1, "Food")
    add_donor_resource(conn, donor_id1, "Clothes")
    print(f"Added donor Bob White with ID: {donor_id1}")

    donor_id2 = add_donor(conn, "Carol Green", "carol@example.com", "10003", "202 Cedar St", "USA", "Can provide shelter and first aid")
    add_donor_resource(conn, donor_id2, "Shelter")
    add_donor_resource(conn, donor_id2, "First Aid")
    print(f"Added donor Carol Green with ID: {donor_id2}\n")

    # 3. Create a match between John Doe and Bob White
    print("Creating match between John Doe and Bob White:")
    match_id1 = mark_as_matched(conn, victim_id1, donor_id1)
    if match_id1:
        print(f"Match created with ID: {match_id1}")
    else:
        print("Failed to create match.")
    
    # 4. Check match status for victims and donors
    print("\nChecking match statuses:")
    print(f"Is John Doe matched? {is_victim_matched(conn, victim_id1)}")  # Expected: True
    print(f"Is Alice Brown matched? {is_victim_matched(conn, victim_id2)}")  # Expected: False
    print(f"Is Bob White matched? {is_donor_matched(conn, donor_id1)}")  # Expected: True
    print(f"Is Carol Green matched? {is_donor_matched(conn, donor_id2)}\n")  # Expected: False

    # 5. Retrieve all victims
    print("Retrieving all victims:")
    all_victims = get_all_victims(conn)
    for victim in all_victims:
        print(dict(victim))

    # 6. Retrieve all donors
    print("\nRetrieving all donors:")
    all_donors = get_all_donors(conn)
    for donor in all_donors:
        print(dict(donor))

    # 7. Retrieve unmatched victims with resources
    print("\nRetrieving unmatched victims with resources:")
    unmatched_victims = get_unmatched_victims_with_resources(conn)
    for victim in unmatched_victims:
        print(victim)

    # 8. Retrieve unmatched donors with resources
    print("\nRetrieving unmatched donors with resources:")
    unmatched_donors = get_unmatched_donors_with_resources(conn)
    for donor in unmatched_donors:
        print(donor)

    # Close the database connection
    close_connection(conn)
    print("\nDatabase connection closed.")
