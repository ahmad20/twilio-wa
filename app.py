import os
import json
import datetime
import pandas as pd
from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Load Google Sheets credentials
SERVICE_ACCOUNT_FILE = "fabled-decker-343201-911e36839265.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)
drive_service = build("drive", "v3", credentials=creds)

# Function to create a new Google Sheet
def create_google_sheet(sheet_name="My Generated Sheet"):
    spreadsheet = {
        "properties": {"title": sheet_name}
    }
    sheet = service.spreadsheets().create(body=spreadsheet, fields="spreadsheetId").execute()
    spreadsheet_id = sheet["spreadsheetId"]

    return spreadsheet_id

# Function to write data to Google Sheets
def write_to_google_sheet(spreadsheet_id, data, sheet_name="Sheet1"):
    sheet_range = f"{sheet_name}!A1"

    # Prepare data for Google Sheets
    body = {
        "values": data
    }

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=sheet_range,
        valueInputOption="RAW",
        body=body
    ).execute()

# Function to read data from Google Sheets
def read_from_google_sheet(spreadsheet_id, sheet_name="Sheet1"):
    sheet_range = f"{sheet_name}!A1:Z100"

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet_range
    ).execute()

    values = result.get("values", [])

    if not values:
        return "No data found."
    else:
        df = pd.DataFrame(values)
        return df.to_dict(orient='records')

@app.route('/create', methods=['POST'])
def create():
    data = request.json
    sheet_name = data.get('sheet_name', 'My Test Sheet')
    spreadsheet_id = create_google_sheet(sheet_name)
    return jsonify({'message': f'Spreadsheet created with ID: {spreadsheet_id}'})

@app.route('/write', methods=['POST'])
def write():
    data = request.json
    spreadsheet_id = data.get('spreadsheet_id')
    data_to_write = data.get('data')
    write_to_google_sheet(spreadsheet_id, data_to_write)
    return jsonify({'message': 'Data written successfully'})

@app.route('/read', methods=['GET'])
def read():
    data = request.args
    spreadsheet_id = data.get('spreadsheet_id')
    result = read_from_google_sheet(spreadsheet_id)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=8080)  # Run on port 8080