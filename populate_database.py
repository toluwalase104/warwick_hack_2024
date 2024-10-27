import sqlite3
import random
from faker import Faker

# Initialize Faker for generating realistic random data
fake = Faker()

# List of real country names
real_countries = [
    "United States", "Canada", "Mexico", "United Kingdom", "France", "Germany", 
    "Italy", "Spain", "Australia", "New Zealand", "Japan", "South Korea", 
    "China", "India", "Brazil", "Argentina", "South Africa", "Egypt", 
    "Nigeria", "Kenya", "Russia", "Turkey", "Saudi Arabia", "Israel", "Sweden",
    "Norway", "Denmark", "Finland", "Netherlands", "Belgium", "Switzerland"
]

# List of possible resource types for victims and donors
resource_types = ["Food", "First Aid", "Shelter", "Clothes", "Money", "Transport"]

def create_victims(conn, num_victims=100):
    """Insert multiple victim records into the database."""
    cursor = conn.cursor()
    victims = []
    for _ in range(num_victims):
        name = fake.name()
        contact = fake.email()
        postcode = fake.zipcode()
        address = fake.address()
        country = random.choice(real_countries)  # Assign a real country
        description = f"Needs {random.choice(resource_types).lower()}"
        completed = random.choice([0, 1])  # Randomly assign if they have been helped

        victims.append((name, contact, postcode, address, country, completed, description))
    
    cursor.executemany("""
        INSERT INTO victims (name, contact, postcode, address, country, completed, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, victims)
    conn.commit()
    print(f"{num_victims} victims inserted.")

def create_requested_resources(conn, num_resources_per_victim=2):
    """Assign random requested resources to each victim, ensuring no duplicates in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM victims")
    victim_ids = [row["id"] for row in cursor.fetchall()]

    for victim_id in victim_ids:
        # Use a set to track assigned resource types within this victim's requests
        assigned_resources = set()

        # Attempt to assign the specified number of unique resources per victim
        while len(assigned_resources) < num_resources_per_victim:
            resource_type = random.choice(resource_types)

            if resource_type not in assigned_resources:
                assigned_resources.add(resource_type)
                
                # Use INSERT OR IGNORE to avoid violating UNIQUE constraint
                cursor.execute("""
                    INSERT OR IGNORE INTO requested_resources (victim_id, resource_type)
                    VALUES (?, ?)
                """, (victim_id, resource_type))
    
    conn.commit()
    print(f"Requested resources assigned to {len(victim_ids)} victims.")

def create_donors(conn, num_donors=50):
    """Insert multiple donor records into the database."""
    cursor = conn.cursor()
    donors = []
    for _ in range(num_donors):
        name = fake.name()
        contact = fake.email()
        postcode = fake.zipcode()
        address = fake.address()
        country = random.choice(real_countries)  # Assign a real country
        description = f"Can provide {random.choice(resource_types).lower()}"
        completed = random.choice([0, 1])  # Randomly assign if they have completed donations

        donors.append((name, contact, postcode, address, country, completed, description))
    
    cursor.executemany("""
        INSERT INTO donors (name, contact, postcode, address, country, completed, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, donors)
    conn.commit()
    print(f"{num_donors} donors inserted.")

def create_donor_resources(conn, num_resources_per_donor=2):
    """Assign random resources that each donor can provide without duplicates in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM donors")
    donor_ids = [row["id"] for row in cursor.fetchall()]

    for donor_id in donor_ids:
        # Use a set to track assigned resource types for each donor
        assigned_resources = set()

        # Attempt to assign the specified number of unique resources per donor
        while len(assigned_resources) < num_resources_per_donor:
            resource_type = random.choice(resource_types)

            if resource_type not in assigned_resources:
                assigned_resources.add(resource_type)
                
                # Use INSERT OR IGNORE to avoid violating UNIQUE constraint
                cursor.execute("""
                    INSERT OR IGNORE INTO donor_resources (donor_id, resource_type)
                    VALUES (?, ?)
                """, (donor_id, resource_type))
    
    conn.commit()
    print(f"Resources assigned to {len(donor_ids)} donors.")

def populate_database():
    """Main function to populate the database with realistic data using real countries."""
    # Connect to the SQLite database
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Allows access by column name

    # Insert data into each table
    create_victims(conn, num_victims=100)
    create_requested_resources(conn, num_resources_per_victim=2)
    create_donors(conn, num_donors=50)
    create_donor_resources(conn, num_resources_per_donor=2)

    # Close the connection
    conn.close()
    print("Database population complete.")

# Run the script
if __name__ == "__main__":
    populate_database()
