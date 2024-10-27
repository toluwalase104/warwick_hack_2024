import database as db
import ai_handler
import smtplib
import time


# ORGANISATION_EMAIL = "crisisCompass@outlook.com"
# ORGANISATION_EMAIL_PASSWORD = "compassCrisis123!"

# NOT WORKING WITH SMTPLIB?
# SHOULD ONLY BE CALLED INSIDE A FUNCTION THAT CALLS THE DATABASE AND CLOSES IT
def send_match_email(conn, victim_id: int, donor_id: int):
    print("Now sending e-mails")
    # user_email = db.get_victim_email(victim_id)

    # donor_email = db.get_donor_email(donor_id)
    # TODO Remove
    # emails = db.get_victim_email(conn, victim_id), db.get_donor_email(conn, donor_id)
    emails = "isaacbode@outlook.com","isaacbode@outlook.com"
    
    print("Email addresses = ", emails)

    for i in range(2):
        session = smtplib.SMTP("smtp-mail.outlook.com", 587)
        session.starttls()
        session.login("crisisCompass@outlook.com", "compassCrisis123!")

        if i == 0:
            message = "Our organisation has successfully found a matching donor for you, we hope that this serves you as well as possible."
        else:
            message = "Your donation has been matched to a recipient, thank you so much for your efforts."

        print(f"Sending message = {message}\nTo {emails[i]}\nFrom {"crisisCompass@outlook.com"}")
        session.sendmail("crisisCompass@outlook.com", emails[i], message)

        session.quit()

def match_donors_and_recipients():
    # Initialize and connect to the database
    conn = db.connect_and_initialize()

    print("Retrieving all victims:")
    all_victims = db.get_all_victims(conn)
    for victim in all_victims:
        print(dict(victim))

    # 6. Retrieve all donors
    print("\nRetrieving all donors:")
    all_donors = db.get_all_donors(conn)
    for donor in all_donors:
        print(dict(donor))
   
    # The variable ``requests`` holds the victim id, their requestewd resources and additional information about their circumstances
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

    # If there are no recipients in need or donors in need, then stop processing
    if len(unmatched_donors) == 0 or len(unmatched_victims) == 0:
        return
    
    # TODO Remove clip in production, should allow for the handling of all requests 
    for i in range( min(1, len(requests)) ):
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
            print("Now considering the line -> ", line)
            line = line.replace("Donor", "").replace("[", "").replace("]", "")
            line = line.split(",")

            try:
                print("Starting try statement")
                line = list(map(lambda x: int(x), line))
                print(line)
                while len(line) > 0 and line[0] in used:
                    print("Removing the used value = ", line.pop(0))

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
        # send_match_email(conn, match[0], match[1])


    # 4. Check match status for victims and donors
    print("\nChecking match statuses:")
    print(f"Is John Doe matched? {db.is_victim_matched(conn, 1)}")  # Expected: True
    print(f"Is Alice Brown matched? {db.is_victim_matched(conn, 2)}")  # Expected: False
    print(f"Is Bob White matched? {db.is_donor_matched(conn, 3)}")  # Expected: True
    print(f"Is Carol Green matched? {db.is_donor_matched(conn, 4)}\n")  # Expected: False

    # Close the database connection
    db.close_connection(conn)
    print("\nDatabase connection closed.")

if __name__ == "__main__":
    match_donors_and_recipients()