
if __name__ == "__main__":
    from database import connect_and_initialize, get_all_donors, get_all_victims, close_connection, a
    conn = connect_and_initialize()

    all_donors = get_all_donors(conn)
    all_victims = get_all_victims(conn)

    print(f"Donors:\n {all_donors}")
    print()
    print(f"Victims: {all_victims}")
    print()

    # donor_resources = all_donor_resources(conn)
    close_connection(conn) 