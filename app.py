import os
import json
import datetime
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Load Google Sheets credentials
SERVICE_ACCOUNT_FILE = "fabled-decker-343201-300066032aff.json"
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

    print(f"✅ New spreadsheet created: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
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

    print(f"✅ Data successfully written to {sheet_name}")

# Function to read data from Google Sheets
def read_from_google_sheet(spreadsheet_id, sheet_name="Sheet1"):
    sheet_range = f"{sheet_name}!A1:Z100"

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet_range
    ).execute()

    values = result.get("values", [])

    if not values:
        print("⚠️ No data found.")
    else:
        df = pd.DataFrame(values)
        print(f"✅ Data from {sheet_name}:\n", df)

def set_public_edit_permissions(spreadsheet_id):
    permission = {
        "type": "anyone",
        "role": "writer"
    }
    drive_service.permissions().create(
        fileId=spreadsheet_id,
        body=permission
    ).execute()
    print(f"✅ Spreadsheet is now public and editable: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")

# Main execution
if __name__ == "__main__":

    pesan = "Ahmad Fauzi, KSM:1, KUR:2, CC:3"
    # parsing pesan
    pesan = pesan.split(", ")
    nama = pesan[0]
    ksm = pesan[1].split(":")[1]
    kur = pesan[2].split(":")[1]
    cc = pesan[3].split(":")[1]

    template = "Nama: {}, KSM: {}, KUR: {}, CC: {}"
    print(template.format(nama, ksm, kur, cc))

    # Step 1: Create a new Google Sheet
    sheet_name = "My Test Sheet"

    spreadsheet_id = create_google_sheet(sheet_name)

    # Step 2: Make it public & editable
    set_public_edit_permissions(spreadsheet_id)

    # Step 4: Write sample data
    sample_data = [
        ["Timestamp", "Nama", "KSM", "KUR", "CC"],
        [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nama, ksm, kur, cc],
    ]
    write_to_google_sheet(spreadsheet_id, sample_data)

    # Step 5: Read data back
    read_from_google_sheet(spreadsheet_id)

