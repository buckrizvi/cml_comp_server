from flask import Flask, request, render_template, send_file, jsonify
import requests
import csv
import io
import os
from dotenv import load_dotenv
from rapidfuzz import fuzz
import logging

# Load environment variables
load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
SECURE_KEY = os.getenv("SECURE_KEY")

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename="/var/www/cml_comp_server/app.log",
    level=logging.WARNING,  # Only log warnings or higher
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def deduplicate_comps(data):
    """Deduplicates records based on distance, acreage, price, and fuzzy address matching."""
    seen = {}
    deduplicated = []

    for item in data:
        comp = item["comp"]
        distance = round(float(item.get("distance", 0.0)), 1)  # Round to 0.1 miles
        acreage = comp.get("acreage", "")
        price = comp.get("price", "")
        address = comp.get("address", "")

        # Create a key for potential duplicates
        key = (distance, acreage, price)

        if key not in seen:
            seen[key] = [address]
            deduplicated.append(item)
        else:
            # Fuzzy match on address
            for existing_address in seen[key]:
                similarity = fuzz.partial_ratio(address, existing_address)
                if similarity >= 90:  # Threshold for matching
                    break
            else:
                seen[key].append(address)
                deduplicated.append(item)

    return deduplicated

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Validate secure key
        key = request.form.get("key")
        if key != SECURE_KEY:
            logging.error("Invalid key entered")
            return jsonify({"error": "Invalid key"}), 403

        try:
            # Parse form inputs
            latitude = request.form.get("latitude")
            longitude = request.form.get("longitude")
            min_acreage = float(request.form.get("min_acreage"))
            max_acreage = float(request.form.get("max_acreage"))
            radius = int(request.form.get("radius"))
            max_comps = int(request.form.get("max_comps"))
            comp_age = int(request.form.get("comp_age"))
            remove_duplicates = request.form.get("remove_duplicates") == "on"

            # Construct payload
            payload = {
                "user_id": "ABCDEF123456",
                "latitude": latitude,
                "longitude": longitude,
                "min_acreage": min_acreage,
                "max_acreage": max_acreage,
                "radius": radius,
                "max_comps": max_comps,
                "comp_options": {
                    "remove_duplicates": remove_duplicates,
                    "comp_age": comp_age
                }
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

                # Log the full response for debugging
                with open("/var/www/cml_comp_server/api_response.log", "w") as log_file:
                    log_file.write(str(results))

                # Deduplicate records
                data = deduplicate_comps(results.get("data", []))

                # Generate CSV
                csv_output = io.StringIO()
                writer = csv.writer(csv_output)

                # Define column order
                headers = ["distance", "status", "price", "acreage", "price_per_acre", "city",
                           "zip_code", "address", "url", "source", "latitude", "longitude",
                           "updated_date", "list_date", "sold_date"]

                writer.writerow(headers)

                for item in data:
                    comp = item.get("comp", {})
                    row = [
                        item.get("distance", ""),  # Distance
                        comp.get("status", ""),   # Status
                        comp.get("price", ""),    # Price
                        comp.get("acreage", ""),  # Acreage
                        comp.get("price_per_acre", ""),
                        comp.get("city", ""),
                        comp.get("zip_code", ""),
                        comp.get("address", ""),
                        comp.get("url", ""),
                        comp.get("source", ""),
                        comp.get("latitude", ""),
                        comp.get("longitude", ""),
                        comp.get("updated_date", ""),
                        comp.get("list_date", ""),
                        comp.get("sold_date", "")
                    ]
                    writer.writerow(row)

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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)