
if __name__ == "__main__":
    from database import connect_and_initialize, get_all_donors, get_all_victims, close_connection, get_unmatched_donors_with_resources
    conn = connect_and_initialize()

    all_donors = get_all_donors(conn)
    all_victims = get_all_victims(conn)

    unmatched_donors = get_unmatched_donors_with_resources(conn)

    print(f"Donors:\n {[[val for val in data] for data in all_donors]}")
    print()
    print(f"Victims: {[[val for val in data] for data in all_victims]}")
    print()
    print(f"Unmatched donors: {unmatched_donors}")
    
    # donor_resources = all_donor_resources(conn)
    close_connection(conn) 