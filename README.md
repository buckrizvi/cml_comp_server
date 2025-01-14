# cml_comp_server
Flask service for comparable properties using the PRYCD.com Comp API with deduplication and CSV export.

## Features
- Dynamic field extraction from API responses.
- Deduplication based on distance, price, and fuzzy matching.
- CSV generation with customizable columns.

## Installation
1. Clone this repository:
git clone https://github.com/buckrizvi/cml_comp_server.

2. Navigate to the project directory:
cd cml_comp_server

3. Create a virtual environment:
python3 -m venv venv
source venv/bin/activate

4. Install dependencies:
pip install -r requirements.txt

## Environment Variables
Create a `.env` file with the following structure:
RAPIDAPI_KEY=your-rapidapi-key
SECURE_KEY=your-secure-key

## Running the Service
1. Start the Flask app using Gunicorn:
gunicorn -w 4 -b 127.0.0.1:5000 app:app

2. Or deploy using a systemd service and Apache.

## Contributions
Feel free to fork this repository and submit pull requests.