from flask import Flask, render_template, request, jsonify 
import database
import matplotlib.pyplot as plt
# import matcher

app = Flask(__name__)


# Home page
@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html")

# Advice page
@app.route("/advice", methods=["POST", "GET"])
def advice():
    return render_template("advice.html")

@app.route("/GPS", methods=["POST","GET"])
def GPS():
    if request.method == "POST":
        data = request.json  # Get the JSON data sent in the request
        # Process the received data as needed
        print(data)

        return jsonify({"message": "Data received successfully!"}), 200
    return render_template("GPS.html")


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

            elif data.get("role") == "donor":
                # Insert the donor into the database
                donor_id = database.add_donor(conn, name, contact, postcode, address, country, description=description)

                # Insert each offered resource type for the donor
                options = data.get("options", [])
                for resource_type in options:
                    database.add_donor_resource(conn, donor_id, resource_type)

                response = {"status": "success", "message": "Donor and resources added successfully."}

            else:
                response = {"status": "error", "message": "Invalid role provided."}

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
    fig, ax = plt.subplots(figsize=(6, 6))  # Adjust size for a smaller PNG output
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%',  
        startangle=140, 
        colors=colors, 
        pctdistance=0.85,   
        wedgeprops=dict(width=0.4)  
    )

    # Create legend and move it below the chart
    plt.legend(
        wedges, [f"{label} ({size})" for label, size in zip(labels, sizes)], 
        title="Items Needed", 
        loc="upper center", 
        bbox_to_anchor=(0.5, -0.1),  # Positions legend below the pie chart
        ncol=2,  # Display in two columns if you have many items
        frameon=False  # Optionally remove legend border for a cleaner look
    )

    # Adjust layout to make space for the legend below
    fig.subplots_adjust(bottom=0.3)

    # Save the figure
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

if __name__ == "__main__":
    app.run(debug=True)