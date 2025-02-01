import gspread
import pandas as pd
import smtplib
import ssl
from google.oauth2.service_account import Credentials
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# 🔹 Load Google Sheets API credentials
SERVICE_ACCOUNT_FILE = "credentials.json"  # Path to your Google API JSON file
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# 🔹 Authenticate with Google Sheets API
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# 🔹 Google Sheet ID and Sheet Name
SPREADSHEET_ID = "1jSpYf7iEZ7HnYf4Ju60dftO3DBGBesfxn6GwJ3jpRVc"  # Update with your actual Google Sheet ID
SHEET_NAME = "Emails"  # Update to match your sheet name

# 🔹 Fetch Data from Google Sheets
def fetch_google_sheet_data():
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    data = sheet.get_all_records()  # Returns data as a list of dictionaries
    return pd.DataFrame(data)  # Convert to Pandas DataFrame

# 🔹 Fetch the latest data
df = fetch_google_sheet_data()

# 🔹 Email credentials
SMTP_SERVER = "smtp-auth.iitb.ac.in"
SMTP_PORT = 587
SENDER_EMAIL = "jay.arora@iitb.ac.in"
ACCESS_TOKEN = "a7b43e5545d0be6a747e03dd91ff6edf"  # Use your generated app password

# 🔹 Follow-up Email Subject & Template
EMAIL_SUBJECT = "Re: Regarding Full-time Opportunities"
EMAIL_TEMPLATE = """\
<html>
 <body style="color: black;">
  
    <p>Dear {first_name},</p>

    <p>I wanted to follow up on my previous email regarding potential <b>full-time opportunities</b> in your organization.</p>

    <p>
      I understand that your schedule may be busy, but I would appreciate any update regarding available roles.
      If you could spare some time, I’d love to discuss further.
    </p>

    <p>Please let me know a convenient time for a quick chat. Looking forward to your response.</p>

    <p>Best Regards,<br>
    Jay Arora<br>
    +91 9784835663</p>
  </body>
</html>
"""

# 🔹 Function to Send Follow-up Emails in the Same Thread
def send_followup_email(receiver_email, first_name, message_id):
    try:
        # Create Follow-up Email Message
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = EMAIL_SUBJECT
        msg["In-Reply-To"] = message_id  # Maintain Threading
        msg["References"] = message_id   # Maintain Threading

        # Personalize the message
        body = EMAIL_TEMPLATE.format(first_name=first_name)
        msg.attach(MIMEText(body, "html"))  # Use HTML format

        # Connect to SMTP Server and Send Email
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)  # Secure the connection
            server.login(SENDER_EMAIL, ACCESS_TOKEN)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())

        print(f"✅ Follow-up email sent to {receiver_email}")

    except Exception as e:
        print(f"❌ Failed to send follow-up email to {receiver_email}: {e}")

# # 🔹 Loop Through Recipients and Send Follow-up Emails
# for index, row in df.iterrows():
#     # Assuming message ID of previous email is stored in a column named "message_id"
#     send_followup_email(row["email"], row["first_name"], row["message_id"])
