from flask import Flask, request, render_template, send_file, jsonify
import requests
import csv
import io
import os
from rapidfuzz import fuzz
import logging

# Load environment variables from Vercel environment
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
SECURE_KEY = os.getenv("SECURE_KEY")

app = Flask(__name__, template_folder='../templates')

# Configure logging for Vercel
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Validate the secure key
        key = request.form.get("key")
        if key != SECURE_KEY:
            logging.error("Invalid key entered")
            return jsonify({"error": "Invalid key"}), 403

        # Parse other form data
        try:
            latitude = request.form.get("latitude")
            longitude = request.form.get("longitude")
            min_acreage = float(request.form.get("min_acreage"))
            max_acreage = float(request.form.get("max_acreage"))
            radius = float(request.form.get("radius"))
            max_comps = int(float(request.form.get("max_comps")))
            comp_age = request.form.get("comp_age")
            remove_duplicates = request.form.get("remove_duplicates") == "on"

            # Construct payload
            comp_options = {}
            if remove_duplicates:
                comp_options["remove_duplicates"] = True
            if comp_age:
                comp_options["comp_age"] = int(float(comp_age))

            payload = {
                "user_id": "ABCDEF123456",
                "latitude": latitude,
                "longitude": longitude,
                "min_acreage": min_acreage,
                "max_acreage": max_acreage,
                "radius": radius,
                "max_comps": max_comps,
                "comp_options": comp_options
            }

            # Call RapidAPI
            API_URL = "https://prycd-comps.p.rapidapi.com/compsByLatLong"
            HEADERS = {
                "x-rapidapi-key": RAPIDAPI_KEY,
                "x-rapidapi-host": "prycd-comps.p.rapidapi.com",
                "Content-Type": "application/json"
            }
            response = requests.post(API_URL, json=payload, headers=HEADERS)
            if response.status_code == 200:
                results = response.json()

                # Generate CSV
                csv_output = io.StringIO()
                writer = csv.writer(csv_output)
                writer.writerow(["Latitude", "Longitude", "Acreage", "Price", "Source"])
                for comp in results.get("data", []):
                    writer.writerow([
                        comp.get("latitude"),
                        comp.get("longitude"),
                        comp.get("acreage"),
                        comp.get("price"),
                        comp.get("source")
                    ])
                csv_output.seek(0)
                return send_file(
                    io.BytesIO(csv_output.getvalue().encode("utf-8")),
                    mimetype="text/csv",
                    as_attachment=True,
                    download_name="comps.csv"
                )
            else:
                logging.error(f"API error: {response.status_code} - {response.text}")
                return jsonify({"error": "API call failed"}), response.status_code
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    return render_template("form.html")

# For local development
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
