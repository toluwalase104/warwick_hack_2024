from flask import Flask, render_template, request, jsonify 
import database
import matplotlib.pyplot as plt
from matcher import match_donors_and_recipients

import time
import multiprocessing

app = Flask(__name__)

#importing the agents
from geolocation import run_geolocation_agent
from google_places import run_google_places_agent

# Home page
@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html")

# calendar page
@app.route("/calendar", methods=["POST", "GET"])
def calendar():
    return render_template("calendar.html")

# Advice page
@app.route("/advice", methods=["POST", "GET"])
def advice():
    return render_template("advice.html")


# Sending data page
@app.route("/resourceRequests", methods=["POST", "GET"])
def resourceRequests():
    if request.method == "POST":
        # Parse incoming JSON data
        data = request.json
        print("Received data:", data)

        # Extract common details
        name = data.get("name")
        contact = data.get("contact")
        address = data.get("address")
        postcode = data.get("postcode")
        country = "UK"  # Assuming country is fixed in this example
        description = data.get("description", "")

        # Initialize and connect to the database
        try:
            conn = database.connect_and_initialize()

            # Check the role and process accordingly
            if data.get("role") == "applicant":
                # Insert the applicant (victim) into the database
                victim_id = database.add_victim(conn, name, contact, postcode, address, country, description=description)

                # Insert each requested resource option for the applicant
                options = data.get("options", [])
                for resource_type in options:
                    database.add_requested_resource(conn, victim_id, resource_type)

                response = {"status": "success", "message": "Applicant and resources added successfully."}

                # match_donors_and_recipients(conn)

            elif data.get("role") == "donor":
                # Insert the donor into the database
                donor_id = database.add_donor(conn, name, contact, postcode, address, country, description=description)

                # Insert each offered resource type for the donor
                options = data.get("options", [])
                for resource_type in options:
                    database.add_donor_resource(conn, donor_id, resource_type)

                response = {"status": "success", "message": "Donor and resources added successfully."}

                # match_donors_and_recipients(conn)

            else:
                response = {"status": "error", "message": "Invalid role provided."}
            
            match_donors_and_recipients(conn)

            conn.close()  # Close the connection after use
            return jsonify(response), 200

        except Exception as e:
            print("Error adding data to database:", e)
            return jsonify({"status": "error", "message": str(e)}), 500

    # If it's a GET request, simply render the resourceRequests.html page
    return render_template("resourceRequests.html")


# Live tracker
@app.route("/liveTracker", methods=["POST", "GET"])
def liveTracker():
    conn = database.connect_and_initialize()
    victimData = database.get_unmatched_victims_with_resources(conn)
    donorData = database.get_unmatched_donors_with_resources(conn)

    # Retrieve all counts
    helped_people_count = database.get_helped_countries_count(conn)
    helped_countries_count = database.get_helped_people_count(conn)
    total_donated_items_count = database.get_helped_countries_count(conn)
    people_needing_help_count = database.get_total_donated_items_count(conn)
    countries_needing_help_count = database.get_countries_needing_help_count(conn)
    resource_counts = sum(database.get_resource_counts(conn).values())
    allOfResources = database.get_resource_counts(conn)

    labels = list(allOfResources.keys())
    sizes = list(allOfResources.values())
    colors = plt.cm.tab20.colors[:len(labels)]

    # Create a smaller figure for the PNG output
    fig, ax = plt.subplots(figsize=(6, 6))

    # Plot pie chart with cleaner settings
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        pctdistance=0.85,
        wedgeprops=dict(width=0.4)
    )

    # Adjust font sizes for labels and percentages for clarity
    for autotext in autotexts:
        autotext.set_fontsize(10)
    for text in texts:
        text.set_fontsize(12)

    # Create and position the legend below the chart
    plt.legend(
        wedges, 
        [f"{label} ({size})" for label, size in zip(labels, sizes)], 
        title="Items Needed", 
        loc="upper center", 
        bbox_to_anchor=(0.5, 0.0),  # Slightly lower for more spacing
        ncol=2,
        frameon=False  # Clean legend look
    )

    # Apply tight layout and save figure
    fig.tight_layout()
    plt.subplots_adjust(bottom=0.3)  # Ensure enough space below chart

    plt.savefig('./static/images/donations.png', format='png', dpi=300, transparent=True, bbox_inches='tight', pad_inches=0.1)
    plt.close()

    createHeatmap = database.plot_helped_countries_heatmap(conn)
    conn.close()    

    return render_template("liveTracker.html", victimData=victimData, donorData=donorData, helped_people_count=helped_people_count,
        helped_countries_count=helped_countries_count,
        total_donated_items_count=total_donated_items_count,
        people_needing_help_count=people_needing_help_count,
        countries_needing_help_count=countries_needing_help_count,
        resource_counts=resource_counts)

# Charities to donate
@app.route("/charities", methods=["POST", "GET"])
def charities():
    return render_template("charities.html")

"""
-----------------------------------------------------
GPS route to process geolocation and POI retrieval --
-----------------------------------------------------
"""
@app.route("/GPS", methods=["POST", "GET"])
def GPS():
    if request.method == "POST":
        # Get the JSON data sent in the request
        data = request.json  

        # Extract variables from received data
        country = data.get("country")
        address = data.get("address")
        items = data.get("items", [])  # Default to an empty list if 'items' isn't provided

        # Determine the main item needed
        item = "shelter"  # Default to shelter
        if items:
            if "shelter" in items:
                item = "shelter"
            elif "medicine" in items:
                item = "medicine"
            elif "water" in items:
                item = "water"
            elif "food" in items:
                item = "food"
            elif "clothes" in items:
                item = "clothes"

        full_address = f"{address}, {country}"
        print(f"Full address: {full_address}")
        print(f"Important item needed: {item}")


        # Call the geolocation agent TODO
        # run_geolocation_agent(full_address) # should show a message

        proc = multiprocessing.Process(target=run_geolocation_agent, args=(full_address))
        print("Starting geolocation agent")
        proc.start()
        print("Sleeping for 20 seconds")
        time.sleep(20)
        proc.terminate()
        print("Terminated geolocation agent")

        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)  # Set the new loop as the current event loop
        # loop.run_until_complete(run_geolocation_agent(full_address))
            

        # Extract latitude and longitude from geolocation.txt
        with open("geolocation.txt", "r") as f:
            coordinates = f.read().split(",")
            latitude = float(coordinates[0])
            longitude = float(coordinates[1])
        print(f"ADDRESS: Latitude: {latitude}, Longitude: {longitude}")

        # Call the google-places agent with the latitude and longitude TODO
        # run_google_places_agent(latitude, longitude)
        # loop.run_until_complete(run_google_places_agent(full_address))
        # loop.close()

        proc = multiprocessing.Process(target=run_google_places_agent, args=(latitude, longitude, item))
        print("Starting google places agent")
        proc.start()
        print("Sleeping for 20 seconds")
        time.sleep(20)
        proc.terminate()
        print("Terminated google places agent")

        # Extract the POIs from google_places.txt and convert to list of dictionaries
        pois = []
        with open("google_places.txt", "r") as f:
            for line in f:
                data = line.strip().split("\t")
                if len(data) == 3: # sanity check
                    poi = {
                        "name": data[0],
                        "latitude": float(data[1]),
                        "longitude": float(data[2])
                    }
                    pois.append(poi)

        print("Parsed POIs:", pois)  # For debugging; you can remove this line later
        # Respond to the client with the POIs
        return jsonify({"message": "Data received and processed successfully!", "pois": pois}), 200
    
    # Render the GPS form if GET request
    return render_template("GPS.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)