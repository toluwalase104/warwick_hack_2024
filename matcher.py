import database as db
import ai_handler
import time

if __name__ == "__main__":
    # Initialize and connect to the database
    conn = db.connect_and_initialize()

    # 1. Add victims and requested resources
    # print("Adding victims and their requested resources:")
    # victim_id1 = db.add_victim(conn, "John Doe", "john@example.com", "12345", "123 Main St", "USA", "Needs food and shelter")
    # db.add_requested_resource(conn, victim_id1, "Food")
    # db.add_requested_resource(conn, victim_id1, "Shelter")
    # print(f"Added victim John Doe with ID: {victim_id1}")

    # victim_id2 = db.add_victim(conn, "Alice Brown", "alice@example.com", "10001", "789 Maple St", "USA", "Needs food and clothes")
    # db.add_requested_resource(conn, victim_id2, "Food")
    # db.add_requested_resource(conn, victim_id2, "Clothes")
    # print(f"Added victim Alice Brown with ID: {victim_id2}\n")

    # 2. Add donors and their available resources
    # print("Adding donors and their available resources:")
    # donor_id1 = db.add_donor(conn, "Bob White", "bob@example.com", "10002", "101 Pine St", "USA", "Can provide food and clothes")
    # db.add_donor_resource(conn, donor_id1, "Food")
    # db.add_donor_resource(conn, donor_id1, "Clothes")
    # print(f"Added donor Bob White with ID: {donor_id1}")

    # donor_id2 = db.add_donor(conn, "Carol Green", "carol@example.com", "10003", "202 Cedar St", "USA", "Can provide shelter and first aid")
    # db.add_donor_resource(conn, donor_id2, "Shelter")
    # db.add_donor_resource(conn, donor_id2, "First Aid")
    # print(f"Added donor Carol Green with ID: {donor_id2}\n")

    # 3. Create a match between John Doe and Bob White
    # print("Creating match between John Doe and Bob White:")
    # match_id1 = db.mark_as_matched(conn, victim_id1, donor_id1)
    # if match_id1:
    #     print(f"Match created with ID: {match_id1}")
    # else:
    #     print("Failed to create match.")
    

    # 5. Retrieve all victims
    print("Retrieving all victims:")
    all_victims = db.get_all_victims(conn)
    for victim in all_victims:
        print(dict(victim))

    # 6. Retrieve all donors
    print("\nRetrieving all donors:")
    all_donors = db.get_all_donors(conn)
    for donor in all_donors:
        print(dict(donor))

    
    # The variable requests holds the victim id, their requestewd resources and additional information about their circumstances
    requests : list[tuple[int, str, str]] = []

    # The variable ``provisions`` holds the donor_id, the resources they offer, and additional related descriptors
    provisions : list[tuple[int, str, str]] = [] 

    # 7. Retrieve unmatched victims with resources
    print("\nRetrieving unmatched victims with resources:")
    unmatched_victims = db.get_unmatched_victims_with_resources(conn)
    for victim in unmatched_victims:
        print(victim)
        requests.append((victim["id"], ", ".join(victim["resources"]), victim["description"]))

    # 8. Retrieve unmatched donors with resources
    print("\nRetrieving unmatched donors with resources:")
    unmatched_donors = db.get_unmatched_donors_with_resources(conn)
    for donor in unmatched_donors:
        print(donor)
        provisions.append((donor["id"], ", ".join(donor["resources"]), donor["description"]))


    print(f"Requests\n {requests}")
    print()
    print(f"Provisions\n {provisions}")
    print()
    print("Sample prompts: ")
    print()
    for i in range( min(2, len(requests)) ):
        # ai_handler.run_query(0, requests, provisions) # Trying claude
        ai_handler.run_query(1, [requests[i]], provisions) # Trying openai
        
        # Gives api some time to rest
        time.sleep(3)
    
    matches : tuple[int, int] = []

    used = set()

    with open("response.txt", "r") as f:
        lines = f.readlines()
        print(lines)
        line_count = 0
        for line in lines:
            line = line.replace("Donor", "").replace("[", "").replace("]", "")
            line = line.split(",")
            try:
                line = list(map(lambda x: int(x), line))

                while len(line) > 0 and line[0] in used:
                    line.pop(0)

                if len(line) > 0:
                    # Map the user id with the matching 
                    matches.append((requests[line_count][0], line[0]))
                    used.add(line[0])

            except Exception as e:
                print(f"Exception {e} occurred whilst reading from file")
                pass

            line_count += 1
    
    for match in matches:
        db.mark_as_matched(conn, match[0], match[1])

    # 4. Check match status for victims and donors
    print("\nChecking match statuses:")
    print(f"Is John Doe matched? {db.is_victim_matched(conn, 1)}")  # Expected: True
    print(f"Is Alice Brown matched? {db.is_victim_matched(conn, 2)}")  # Expected: False
    print(f"Is Bob White matched? {db.is_donor_matched(conn, 3)}")  # Expected: True
    print(f"Is Carol Green matched? {db.is_donor_matched(conn, 4)}\n")  # Expected: False

    # Close the database connection
    db.close_connection(conn)
    print("\nDatabase connection closed.")
    