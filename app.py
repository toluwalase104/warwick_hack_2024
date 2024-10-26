from flask import Flask, render_template, request, jsonify 
import database

app = Flask(__name__)


# Home page
@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html")

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
    res = database.get_unmatched_victims_with_resources(conn)
    conn.close()
    return res
    #return render_template("liveTracker.html")

# Charities to donate
@app.route("/charities", methods=["POST", "GET"])
def charities():
    return render_template("charities.html")

if __name__ == "__main__":
    app.run(debug=True)