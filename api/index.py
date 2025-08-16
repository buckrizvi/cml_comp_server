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
        debug_info = {
            "environment_variables": {},
            "form_data": {},
            "payload": {},
            "api_response": {},
            "csv_data": {},
            "errors": []
        }
        
        # Check environment variables
        debug_info["environment_variables"] = {
            "RAPIDAPI_KEY": "✅ Set" if RAPIDAPI_KEY else "❌ Missing",
            "RAPIDAPI_KEY_length": len(RAPIDAPI_KEY) if RAPIDAPI_KEY else 0,
            "RAPIDAPI_KEY_preview": f"{RAPIDAPI_KEY[:8]}..." if RAPIDAPI_KEY and len(RAPIDAPI_KEY) > 8 else RAPIDAPI_KEY,
            "SECURE_KEY": "✅ Set" if SECURE_KEY else "❌ Missing",
            "SECURE_KEY_length": len(SECURE_KEY) if SECURE_KEY else 0
        }
        
        # Validate the secure key
        key = request.form.get("key")
        debug_info["form_data"]["entered_key"] = f"{key[:3]}..." if key and len(key) > 3 else key
        debug_info["form_data"]["key_match"] = key == SECURE_KEY
        
        if key != SECURE_KEY:
            debug_info["errors"].append("❌ Invalid secure key entered")
            return render_template("debug.html", debug_info=debug_info)

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

            debug_info["form_data"] = {
                "latitude": latitude,
                "longitude": longitude,
                "min_acreage": min_acreage,
                "max_acreage": max_acreage,
                "radius": radius,
                "max_comps": max_comps,
                "comp_age": comp_age,
                "remove_duplicates": remove_duplicates
            }

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
            
            debug_info["payload"] = payload

            # Call RapidAPI
            API_URL = "https://prycd-comps.p.rapidapi.com/compsByLatLong"
            HEADERS = {
                "x-rapidapi-key": RAPIDAPI_KEY,
                "x-rapidapi-host": "prycd-comps.p.rapidapi.com",
                "Content-Type": "application/json"
            }
            
            debug_info["api_request"] = {
                "url": API_URL,
                "headers": {
                    "x-rapidapi-key": f"{RAPIDAPI_KEY[:8]}..." if RAPIDAPI_KEY else "Missing",
                    "x-rapidapi-host": "prycd-comps.p.rapidapi.com",
                    "Content-Type": "application/json"
                },
                "method": "POST"
            }
            
            response = requests.post(API_URL, json=payload, headers=HEADERS)
            
            debug_info["api_response"] = {
                "status_code": response.status_code,
                "status_text": "✅ Success" if response.status_code == 200 else f"❌ Error {response.status_code}",
                "headers": dict(response.headers),
                "response_size": len(response.content),
                "response_text": response.text[:1000] + "..." if len(response.text) > 1000 else response.text
            }
            
            if response.status_code == 200:
                try:
                    results = response.json()
                    debug_info["api_response"]["json_parsed"] = "✅ Successfully parsed JSON"
                    debug_info["api_response"]["response_structure"] = {
                        "keys": list(results.keys()) if isinstance(results, dict) else "Not a dictionary",
                        "data_type": str(type(results)),
                        "data_length": len(results) if hasattr(results, '__len__') else "No length"
                    }
                    
                    # Check if data exists and what's in it
                    data = results.get("data", [])
                    debug_info["csv_data"] = {
                        "data_found": "✅ Yes" if data else "❌ No",
                        "data_count": len(data) if isinstance(data, list) else 0,
                        "data_type": str(type(data)),
                        "first_item_keys": list(data[0].keys()) if data and isinstance(data, list) and len(data) > 0 else "No data items",
                        "sample_data": data[:2] if isinstance(data, list) and len(data) > 0 else "No sample data available"
                    }

                    # Generate CSV
                    csv_output = io.StringIO()
                    writer = csv.writer(csv_output)
                    writer.writerow(["Latitude", "Longitude", "Acreage", "Price", "Source"])
                    csv_rows_written = 0
                    for comp in data:
                        writer.writerow([
                            comp.get("latitude"),
                            comp.get("longitude"),
                            comp.get("acreage"),
                            comp.get("price"),
                            comp.get("source")
                        ])
                        csv_rows_written += 1
                    
                    debug_info["csv_data"]["rows_written"] = csv_rows_written
                    debug_info["csv_data"]["csv_content_preview"] = csv_output.getvalue()[:500]
                    
                    csv_output.seek(0)
                    
                    # Check if user wants debug mode or CSV download
                    if request.form.get("download_csv") == "yes":
                        return send_file(
                            io.BytesIO(csv_output.getvalue().encode("utf-8")),
                            mimetype="text/csv",
                            as_attachment=True,
                            download_name="comps.csv"
                        )
                    elif request.form.get("debug_mode") == "on":
                        # Show debug information
                        return render_template("debug.html", debug_info=debug_info)
                    else:
                        # Default behavior: download CSV if data found, show debug if no data
                        if csv_rows_written > 0:
                            return send_file(
                                io.BytesIO(csv_output.getvalue().encode("utf-8")),
                                mimetype="text/csv",
                                as_attachment=True,
                                download_name="comps.csv"
                            )
                        else:
                            # No data found, show debug info to help troubleshoot
                            debug_info["errors"].append("❌ No data found - showing debug information to help troubleshoot")
                            return render_template("debug.html", debug_info=debug_info)
                        
                except Exception as json_error:
                    debug_info["errors"].append(f"❌ JSON parsing failed: {str(json_error)}")
                    debug_info["api_response"]["json_parsed"] = f"❌ Failed: {str(json_error)}"
                    return render_template("debug.html", debug_info=debug_info)
            else:
                debug_info["errors"].append(f"❌ API call failed with status {response.status_code}")
                return render_template("debug.html", debug_info=debug_info)
                
        except Exception as e:
            debug_info["errors"].append(f"❌ Unexpected error: {str(e)}")
            return render_template("debug.html", debug_info=debug_info)

    return render_template("form.html")

# For local development
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
