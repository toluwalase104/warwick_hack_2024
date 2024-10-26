from flask import Flask, render_template, request, jsonify 

app = Flask(__name__)

# Home page
@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html")

# Sending data page
@app.route("/resourceRequests", methods=["POST", "GET"])
def resourceRequests():
    return render_template("resourceRequests.html")

# Live tracker
@app.route("/liveTracker", methods=["POST", "GET"])
def liveTracker():
    return render_template("liveTracker.html")

# Charities to donate
@app.route("/charities", methods=["POST", "GET"])
def charities():
    return render_template("charities.html")

if __name__ == "__main__":
    app.run(debug=True)