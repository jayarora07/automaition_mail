import gspread
import pandas as pd
import subprocess
import sys
import os
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

# ✅ Fix ImportError: Use Absolute Import or Modify Path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))  
from Follow_up import send_followup_email  # Import follow-up function

# 🔹 Google Sheets API Credentials
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# 🔹 Google Sheets Configuration
SPREADSHEET_ID = "1jSpYf7iEZ7HnYf4Ju60dftO3DBGBesfxn6GwJ3jpRVc"
SHEET_NAME = "Emails"

# 🔹 Authenticate with Google Sheets API
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# 🔹 Function to Fetch Data from Google Sheets
def fetch_google_sheet_data():
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# 🔹 Function to Check for Emails Needing Follow-up
def check_followup_emails(df):
    today_date = datetime.now().date()
    followup_list = []

    for index, row in df.iterrows():
        try:
            # Convert "Mail_sent_on" to a date object
            mail_sent_date = datetime.strptime(row["Mail_sent_on"], "%d-%m-%y").date()

            # Check if it's exactly 5 days old and status is "Mail sent"
            if (today_date - mail_sent_date).days >= 5 and row["Status"] == "Mail sent":
                followup_list.append({
                    "index": index,
                    "email": row["email"],
                    "first_name": row["first_name"],
                    "message_id": row["message_id"]
                })
        
        except ValueError:
            print(f"❌ Skipping invalid date format: {row['Mail_sent_on']} for {row['email']}")

    return followup_list

# 🔹 Function to Update Status & "R1_sent_on" Date in Google Sheets
def update_followup_status(followup_list):
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    today_date = datetime.now().strftime("%d-%m-%y")  # 🔹 Format: DD-MM-YY

    for followup in followup_list:
        row_index = followup["index"] + 2  # Adjust for 0-based index

        # Update "Status" to "R1 sent"
        sheet.update_cell(row_index, 6, "R1 sent")  # Column F (6th column)
        
        # Update "R1_sent_on" with today's date
        sheet.update_cell(row_index, 7, today_date)  # Column G (7th column)

        print(f"🔄 Updated 'Status' to 'R1 sent' and 'R1_sent_on' to {today_date} for {followup['email']}")

# 🔹 Main Execution
def main():
    df = fetch_google_sheet_data()
    followup_list = check_followup_emails(df)

    if followup_list:
        print("\n✅ The following emails qualify for follow-up:")
        for followup in followup_list:
            send_followup_email(followup["email"], followup["first_name"], followup["message_id"])
            print(followup["email"])

        # 🔹 Update Status & Follow-up Sent Date
        update_followup_status(followup_list)


    else:
        print("❌ No emails qualify for follow-up today.")

if __name__ == "__main__":
    main()
