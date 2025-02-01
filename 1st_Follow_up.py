import gspread
import pandas as pd
import subprocess
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
from Follow_up import send_followup_email


# 🔹 Google Sheets API Credentials
SERVICE_ACCOUNT_FILE = "credentials.json"  # Path to your Google API JSON file
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# 🔹 Google Sheets Configuration
SPREADSHEET_ID = "1jSpYf7iEZ7HnYf4Ju60dftO3DBGBesfxn6GwJ3jpRVc"  # Replace with your actual Google Sheet ID
SHEET_NAME = "Emails"  # Change to match your sheet's name

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
    today_date = datetime.now().date()  # Get today's date (without time)
    followup_list = []

    for index, row in df.iterrows():
        try:
            # Convert "Mail_sent_on" to a date object
            mail_sent_date = datetime.strptime(row["Mail_sent_on"], "%d-%m-%y").date()

            # Check if it's exactly 5 days old and status is "Mail sent"
            if (today_date - mail_sent_date).days >= 5 and row["Status"] == "Mail sent":
                followup_list.append({
                    "email": row["email"],
                    "first_name": row["first_name"],
                    "message_id": row["message_id"]
                })
        
        except ValueError:
            print(f"❌ Skipping invalid date format: {row['Mail_sent_on']} for {row['email']}")

    return followup_list

# 🔹 Main Execution
def main():
    df = fetch_google_sheet_data()
    followup_list = check_followup_emails(df)

    if followup_list:
        print("\n✅ The following emails qualify for follow-up:")
        for email in followup_list:
            send_followup_email(email["email"], email["first_name"], email["message_id"])
            print(email)

        

    else:
        print("❌ No emails qualify for follow-up today.")

if __name__ == "__main__":
    main()
