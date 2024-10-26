import sqlite3
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

def connect_and_initialize(db_path="database.db", schema_path="schema.sql"):
    """
    Connects to the SQLite database and initializes it using the schema provided in schema.sql.

    Parameters:
    - db_path: The path to the database file (default is "database.db").
    - schema_path: The path to the schema SQL file to initialize tables (default is "schema.sql").

    Returns:
    - conn: SQLite database connection.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Allows row access by column name
    cursor = conn.cursor()
    with open(schema_path, 'r') as f:
        schema = f.read()
    cursor.executescript(schema)
    conn.commit()
    return conn

def add_victim(conn, name, contact, postcode, address, country, description=""):
    """
    Adds a new victim entry to the database.

    Parameters:
    - conn: SQLite database connection.
    - name: Victim's name.
    - contact: Contact information of the victim.
    - postcode: Victim's postal code.
    - address: Victim's address.
    - country: Victim's country.
    - description: Additional information about the victim's needs.

    Returns:
    - The ID of the inserted victim row.
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO victims (name, contact, postcode, address, country, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, contact, postcode, address, country, description))
    conn.commit()
    return cursor.lastrowid

def add_requested_resource(conn, victim_id, resource_type):
    """
    Adds a requested resource for a specific victim.

    Parameters:
    - conn: SQLite database connection.
    - victim_id: The ID of the victim.
    - resource_type: The type of resource requested by the victim.

    Returns:
    - The ID of the inserted requested resource row.
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO requested_resources (victim_id, resource_type)
        VALUES (?, ?)
    """, (victim_id, resource_type))
    conn.commit()
    return cursor.lastrowid

def add_donor(conn, name, contact, postcode, address, country, description=""):
    """
    Adds a new donor entry to the database.

    Parameters:
    - conn: SQLite database connection.
    - name: Donor's name.
    - contact: Contact information of the donor.
    - postcode: Donor's postal code.
    - address: Donor's address.
    - country: Donor's country.
    - description: Additional information about the donor.

    Returns:
    - The ID of the inserted donor row.
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO donors (name, contact, postcode, address, country, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, contact, postcode, address, country, description))
    conn.commit()
    return cursor.lastrowid

def add_donor_resource(conn, donor_id, resource_type):
    """
    Adds a resource that a donor can provide.

    Parameters:
    - conn: SQLite database connection.
    - donor_id: The ID of the donor.
    - resource_type: The type of resource the donor can provide.

    Returns:
    - The ID of the inserted donor resource row.
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO donor_resources (donor_id, resource_type)
        VALUES (?, ?)
    """, (donor_id, resource_type))
    conn.commit()
    return cursor.lastrowid

def add_match(conn, resource_id, donor_resource_id):
    """
    Creates a match between a requested resource and a donor's resource.

    Parameters:
    - conn: SQLite database connection.
    - resource_id: The ID of the requested resource.
    - donor_resource_id: The ID of the donor's resource.

    Returns:
    - The ID of the inserted match row.
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO matches (resource_id, donor_resource_id)
        VALUES (?, ?)
    """, (resource_id, donor_resource_id))
    conn.commit()
    return cursor.lastrowid

def get_all_victims(conn):
    """
    Retrieves all victims from the database.

    Parameters:
    - conn: SQLite database connection.

    Returns:
    - List of all victims with their details.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM victims")
    return cursor.fetchall()

def get_all_donors(conn):
    """
    Retrieves all donors from the database.

    Parameters:
    - conn: SQLite database connection.

    Returns:
    - List of all donors with their details.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    return cursor.fetchall()

def mark_as_matched(conn, victim_id, donor_id):
    """
    Marks a victim and a donor as matched and updates their completion status.

    Parameters:
    - conn: SQLite database connection.
    - victim_id: The ID of the victim.
    - donor_id: The ID of the donor.

    Returns:
    - The ID of the created match entry.
    """
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO matches (victim_id, donor_id)
            VALUES (?, ?)
        """, (victim_id, donor_id))
        conn.commit()
        match_id = cursor.lastrowid
        cursor.execute("UPDATE victims SET completed = 1 WHERE id = ?", (victim_id,))
        cursor.execute("UPDATE donors SET completed = 1 WHERE id = ?", (donor_id,))
        conn.commit()
        return match_id
    except sqlite3.IntegrityError as e:
        print("Error marking as matched:", e)
        return None

def get_unmatched_victims_with_resources(conn):
    """
    Retrieves all unmatched victims with their requested resources.

    Parameters:
    - conn: SQLite database connection.

    Returns:
    - List of dictionaries, where each dictionary represents an unmatched victim with all details and a list of their requested resources.
    """
    cursor = conn.cursor()
    query = """
        SELECT victims.*, requested_resources.resource_type
        FROM victims
        JOIN requested_resources ON victims.id = requested_resources.victim_id
        WHERE victims.completed = 0
    """
    cursor.execute(query)
    victim_dict = defaultdict(lambda: {
        "id": None,
        "name": "",
        "contact": "",
        "postcode": "",
        "address": "",
        "country": "",
        "completed": 0,
        "description": "",
        "resources": []
    })
    
    for row in cursor.fetchall():
        victim_id = row["id"]
        victim_dict[victim_id]["id"] = row["id"]
        victim_dict[victim_id]["name"] = row["name"]
        victim_dict[victim_id]["contact"] = row["contact"]
        victim_dict[victim_id]["postcode"] = row["postcode"]
        victim_dict[victim_id]["address"] = row["address"]
        victim_dict[victim_id]["country"] = row["country"]
        victim_dict[victim_id]["completed"] = row["completed"]
        victim_dict[victim_id]["description"] = row["description"]
        victim_dict[victim_id]["resources"].append(row["resource_type"])
    return list(victim_dict.values())

def get_unmatched_donors_with_resources(conn):
    """
    Retrieves all unmatched donors with the resources they can provide.

    Parameters:
    - conn: SQLite database connection.

    Returns:
    - List of dictionaries, where each dictionary represents an unmatched donor with all details and a list of resources they can provide.
    """

    cursor = conn.cursor()
    query = """
        SELECT donors.*, donor_resources.resource_type
        FROM donors
        JOIN donor_resources ON donors.id = donor_resources.donor_id
        WHERE donors.completed = 0
    """
    
    cursor.execute(query)
    donor_dict = defaultdict(lambda: {
        "id": None,
        "name": "",
        "contact": "",
        "postcode": "",
        "address": "",
        "country": "",
        "completed": 0,
        "description": "",
        "resources": []
    })
    
    for row in cursor.fetchall():
        donor_id = row["id"]
        donor_dict[donor_id]["id"] = row["id"]
        donor_dict[donor_id]["name"] = row["name"]
        donor_dict[donor_id]["contact"] = row["contact"]
        donor_dict[donor_id]["postcode"] = row["postcode"]
        donor_dict[donor_id]["address"] = row["address"]
        donor_dict[donor_id]["country"] = row["country"]
        donor_dict[donor_id]["completed"] = row["completed"]
        donor_dict[donor_id]["description"] = row["description"]
        donor_dict[donor_id]["resources"].append(row["resource_type"])
    return list(donor_dict.values())

def is_victim_matched(conn, victim_id):
    """
    Checks if a victim has been matched by examining their `completed` status.

    Parameters:
    - conn: SQLite database connection
    - victim_id: The ID of the victim to check

    Returns:
    - True if the victim has been matched (completed = 1), False otherwise.
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
    - True if the donor has been matched (completed = 1), False otherwise.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT completed FROM donors WHERE id = ?", (donor_id,))
    result = cursor.fetchone()
    return result is not None and result[0] == 1

def get_resource_counts(conn):
    """
    Retrieves the count of each type of resource requested by victims.

    Parameters:
    - conn: SQLite database connection.

    Returns:
    - A dictionary with resource types as keys and the count of each resource as values.
    """
    cursor = conn.cursor()
    query = """
        SELECT resource_type, COUNT(*) AS count
        FROM requested_resources
        GROUP BY resource_type
    """
    cursor.execute(query)
    
    # Convert the result to a dictionary
    resource_counts = {row["resource_type"]: row["count"] for row in cursor.fetchall()}
    return resource_counts

def get_to_help_countries_counts(conn):
    """
    Retrieves the count of resources in waiting list to be received by each country that has received aid.

    Parameters:
    - conn: SQLite database connection.

    Returns:
    - A dictionary where keys are country names and values are the count of resources received by that country.
    """
    cursor = conn.cursor()
    query = """
        SELECT victims.country, COUNT(requested_resources.id) AS resources_count
        FROM victims
        JOIN requested_resources ON victims.id = requested_resources.victim_id
        WHERE victims.completed = 0
        GROUP BY victims.country
    """
    cursor.execute(query)
    
    # Convert the result to a dictionary
    country_counts = {row["country"]: row["resources_count"] for row in cursor.fetchall()}
    return country_counts

def get_helped_countries_counts(conn):
    """
    Retrieves the count of resources received by each country that has received aid.

    Parameters:
    - conn: SQLite database connection.

    Returns:
    - A dictionary where keys are country names and values are the count of resources received by that country.
    """
    cursor = conn.cursor()
    query = """
        SELECT victims.country, COUNT(requested_resources.id) AS resources_count
        FROM victims
        JOIN requested_resources ON victims.id = requested_resources.victim_id
        WHERE victims.completed = 1
        GROUP BY victims.country
    """
    cursor.execute(query)
    
    # Convert the result to a dictionary
    country_counts = {row["country"]: row["resources_count"] for row in cursor.fetchall()}
    return country_counts

def get_helped_people_count(conn):
    """
    Retrieves the count of victims who have been marked as completed (i.e., helped).

    Parameters:
    - conn: SQLite database connection.

    Returns:
    - An integer representing the count of people who have been helped.
    """
    cursor = conn.cursor()
    query = """
        SELECT COUNT(*) AS helped_count
        FROM victims
        WHERE completed = 1
    """
    cursor.execute(query)
    
    # Fetch the count result
    result = cursor.fetchone()
    return result["helped_count"] if result else 0

def get_helped_countries_count(conn):
    """
    Retrieves the count of unique countries where people have been helped.

    Parameters:
    - conn: SQLite database connection.

    Returns:
    - An integer representing the count of unique countries where people have been helped.
    """
    cursor = conn.cursor()
    query = """
        SELECT COUNT(DISTINCT country) AS country_count
        FROM victims
        WHERE completed = 1
    """
    cursor.execute(query)
    
    # Fetch the country count result
    result = cursor.fetchone()
    return result["country_count"] if result else 0

def get_total_donated_items_count(conn):
    """
    Retrieves the total count of items donated across all resource types.

    Parameters:
    - conn: SQLite database connection.

    Returns:
    - An integer representing the total count of items donated.
    """
    cursor = conn.cursor()
    query = """
        SELECT COUNT(*) AS total_donated_items
        FROM donor_resources
    """
    cursor.execute(query)
    
    # Fetch the total count of donated items
    result = cursor.fetchone()
    return result["total_donated_items"] if result else 0

def get_people_needing_help_count(conn):
    """
    Retrieves the count of victims who still need help (i.e., not marked as completed).

    Parameters:
    - conn: SQLite database connection.

    Returns:
    - An integer representing the count of people who still need help.
    """
    cursor = conn.cursor()
    query = """
        SELECT COUNT(*) AS needing_help_count
        FROM victims
        WHERE completed = 0
    """
    cursor.execute(query)
    
    # Fetch the count of people who still need help
    result = cursor.fetchone()
    return result["needing_help_count"] if result else 0

def get_countries_needing_help_count(conn):
    """
    Retrieves the count of unique countries where people still need help.

    Parameters:
    - conn: SQLite database connection.

    Returns:
    - An integer representing the count of unique countries where people still need help.
    """
    cursor = conn.cursor()
    query = """
        SELECT COUNT(DISTINCT country) AS countries_needing_help_count
        FROM victims
        WHERE completed = 0
    """
    cursor.execute(query)
    
    # Fetch the count of countries where help is still needed
    result = cursor.fetchone()
    return result["countries_needing_help_count"] if result else 0

def get_people_needing_help_count(conn):
    """
    Retrieves the count of victims who still need help (i.e., not marked as completed).

    Parameters:
    - conn: SQLite database connection.

    Returns:
    - An integer representing the count of people who still need help.
    """
    cursor = conn.cursor()
    query = """
        SELECT COUNT(*) AS needing_help_count
        FROM victims
        WHERE completed = 0
    """
    cursor.execute(query)
    
    # Fetch the count of people who still need help
    result = cursor.fetchone()
    return result["needing_help_count"] if result else 0


def close_connection(conn):
    """
    Closes the SQLite database connection.

    Parameters:
    - conn: SQLite database connection to be closed.

    Returns:
    - None
    """
    conn.close()

def plot_to_help_countries_heatmap(conn):
    # Step 1: Get the count of resources distributed by country
    country_counts = get_to_help_countries_counts(conn)
    
    # Step 2: Convert to DataFrame
    df = pd.DataFrame(list(country_counts.items()), columns=["country", "count"])

    # Optional: Standardize country names to match shapefile names
    country_rename_map = {
        "United States": "United States of America",
        "Russia": "Russian Federation",
        # Add any other necessary mappings here
    }
    df["country"] = df["country"].replace(country_rename_map)

    # Load the world map shapefile
    world = gpd.read_file("./data/ne_110m_admin_0_countries.shp")

    # Merge the world map with the data on country names
    merged = world.set_index("NAME").join(df.set_index("country"), how="left")

    # Fill NaN values in 'count' with 0 for countries with no data
    merged["count"] = merged["count"].fillna(0)

    # Check for unmatched countries to identify potential mismatches
    unmatched = merged[merged["count"] == 0]
    print("Unmatched countries with no data:", unmatched.index.tolist())

    # Save the plot to a file instead of showing it
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    merged.plot(column="count", cmap="OrRd", linewidth=0.8, ax=ax, edgecolor="0.8", legend=True)
    ax.set_title("Resources to be Distributed by Country")
    plt.savefig("./static/images/to_help_countries_heatmap.png", format='png', dpi=300, transparent=True)
    plt.close()

def plot_helped_countries_heatmap(conn):
    # Step 1: Get the count of resources distributed by country
    country_counts = get_helped_countries_counts(conn)
    
    # Step 2: Convert to DataFrame
    df = pd.DataFrame(list(country_counts.items()), columns=["country", "count"])

    # Optional: Standardize country names to match shapefile names
    country_rename_map = {
        "United States": "United States of America",
        "Russia": "Russian Federation",
        # Add any other necessary mappings here
    }
    df["country"] = df["country"].replace(country_rename_map)

    # Load the world map shapefile
    world = gpd.read_file("./data/ne_110m_admin_0_countries.shp")

    # Merge the world map with the data on country names
    merged = world.set_index("NAME").join(df.set_index("country"), how="left")

    # Fill NaN values in 'count' with 0 for countries with no data
    merged["count"] = merged["count"].fillna(0)

    # Check for unmatched countries to identify potential mismatches
    unmatched = merged[merged["count"] == 0]
    print("Unmatched countries with no data:", unmatched.index.tolist())

    # Save the plot to a file instead of showing it
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    merged.plot(column="count", cmap="OrRd", linewidth=0.8, ax=ax, edgecolor="0.8", legend=True)
    ax.set_title("Resources Distributed by Country")
    plt.savefig("./static/images/helped_countries_heatmap.png", format='png', dpi=300, transparent=True)
    plt.close()

if __name__ == "__main__":
    # Connect to the database and initialize schema (assuming connect_and_initialize is defined)
    conn = connect_and_initialize()
    
    # Add victims from different countries
    victim_id1 = add_victim(conn, "Alice", "alice@example.com", "12345", "123 Street", "USA", "Needs food")
    victim_id2 = add_victim(conn, "Bob", "bob@example.com", "54321", "456 Avenue", "Canada", "Needs shelter")
    victim_id3 = add_victim(conn, "Carlos", "carlos@example.com", "67890", "789 Boulevard", "Mexico", "Needs clothes")
    victim_id4 = add_victim(conn, "Diana", "diana@example.com", "13579", "101 Road", "USA", "Needs food and shelter")

    # Add requested resources for each victim
    add_requested_resource(conn, victim_id1, "Food")
    add_requested_resource(conn, victim_id2, "Shelter")
    add_requested_resource(conn, victim_id3, "Clothes")
    add_requested_resource(conn, victim_id4, "Food")
    # add_requested_resource(conn, victim_id4, "Shelter")

    # Add donors from different countries
    donor_id1 = add_donor(conn, "Earnest", "earnest@example.com", "12345", "123 Street", "USA", "Offers food for 8")
    donor_id2 = add_donor(conn, "Fiona", "fiona@example.com", "54321", "456 Avenue", "Canada", "Offers shelter for 5")
    donor_id3 = add_donor(conn, "George", "george@example.com", "67890", "789 Boulevard", "Mexico", "Offers medium-sized clothes")
    donor_id4 = add_donor(conn, "Helen", "helen@example.com", "13579", "101 Road", "USA", "Offers canned-foods and shelter")

    # Add requested resources for each victim
    add_donor_resource(conn, donor_id1, "Food")
    add_donor_resource(conn, donor_id2, "Shelter")
    add_donor_resource(conn, donor_id3, "Clothes")
    add_donor_resource(conn, donor_id4, "Food")
    # add_donor_resource(conn, victim_id4, "Shelter")

    # Mark some victims as helped (completed)
    # mark_as_matched(conn, victim_id1, donor_id1)  # Assuming donor_id=1 is available
    # mark_as_matched(conn, victim_id2, donor_id2)  # Assuming donor_id=2 is available
    # mark_as_matched(conn, victim_id4, donor_id=3)  # Assuming donor_id=3 is available

    # Run the function to get helped countries' counts
    # result = get_helped_countries_counts(conn)

    # Expected result should be:
    # USA -> 3 (Alice's Food + Diana's Food + Diana's Shelter)
    # Canada -> 1 (Bob's Shelter)
    # print("Helped Countries Counts:", result)

    # plot_helped_countries_heatmap(conn)
    # plot_to_help_countries_heatmap(conn)


    # Close the connection
    close_connection(conn)
"""
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
"""