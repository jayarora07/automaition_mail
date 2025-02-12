import imaplib
import email
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from email.header import decode_header
from datetime import datetime, timedelta
import ssl

# 🔹 IMAP Credentials for IITB Webmail
IMAP_SERVER = "imap.iitb.ac.in"
IMAP_PORT = 993
EMAIL_ID = "jay.arora@iitb.ac.in"
ACCESS_TOKEN = "a7b43e5545d0be6a747e03dd91ff6edf"

# 🔹 Google Sheets API Credentials
SERVICE_ACCOUNT_FILE = "credentials.json"  # Path to your Google API JSON file
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# 🔹 Google Sheets Configuration
SPREADSHEET_ID = "1jSpYf7iEZ7HnYf4Ju60dftO3DBGBesfxn6GwJ3jpRVc"  # Replace with your actual Google Sheet ID
SHEET_NAME = "Emails"  # Change to match your sheet's name

# 🔹 Function to Fetch Sent Emails List from Google Sheets
def fetch_sent_emails():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    data = sheet.get_all_records()
    
    df = pd.DataFrame(data)  # Convert to DataFrame
    return df, set(df["email"])  # Convert email column to a set

# 🔹 Function to Connect to IITB Webmail (IMAP)
def connect_to_imap():
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT, ssl_context=context)
        mail.login(EMAIL_ID, ACCESS_TOKEN)
        print("✅ Logged in to IITB Webmail successfully!")
        return mail
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

# 🔹 Function to Fetch Recent Email Senders
def fetch_recent_emails(mail):
    try:
        mail.select("INBOX")
        # Get date 48 hours ago
        date_since = (datetime.now() - timedelta(hours=1)).strftime("%d-%b-%Y")
        query = f'(SINCE {date_since})'
        
        status, messages = mail.search(None, query)
        if status != "OK":
            print("❌ Error fetching emails")
            return set()

        replied_emails = set()

        for num in messages[0].split():
            status, msg_data = mail.fetch(num, "(RFC822)")
            if status != "OK":
                continue
                
            email_body = msg_data[0][1]
            email_msg = email.message_from_bytes(email_body)

            # Extract sender's email
            sender = email.utils.parseaddr(email_msg["From"])[1]
            if sender:
                replied_emails.add(sender)

        return replied_emails

    except Exception as e:
        print(f"❌ Error while fetching emails: {e}")
        return set()

# 🔹 Function to Update Status in Google Sheets (Always Change to "Replied")
def update_status_in_sheets(df, matched_emails):
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

    for index, row in df.iterrows():
        if row["email"] in matched_emails:
            sheet.update_cell(index + 2, 6, "Replied")  # Column F (6th column)
            print(f"🔄 Updated status to 'Replied' for {row['email']}")

# 🔹 Main Execution
def main():
    mail = connect_to_imap()
    if mail:
        # Fetch replied email IDs from IITB Webmail
        replied_emails = fetch_recent_emails(mail)
        
        # Fetch email list from Google Sheets
        df, sent_email_list = fetch_sent_emails()
        
        # Compare and find matching emails
        matched_emails = replied_emails.intersection(sent_email_list)

        mail.logout()
        print("\n✅ Logged out successfully")

        # Print emails that replied and exist in the spreadsheet
        if matched_emails:
            print("\n✅ Email IDs that replied and are in the spreadsheet:")
            for email_id in matched_emails:
                print(email_id)

            # 🔹 Update Status Column in Google Sheets (Always Set to "Replied")
            update_status_in_sheets(df, matched_emails)
        else:
            print("❌ No matching replies found in the spreadsheet.")

if __name__ == "__main__":
    main()
