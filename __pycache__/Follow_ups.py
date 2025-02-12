import gspread
import pandas as pd
import sys
import os
import smtplib
import ssl
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# ✅ Fix ImportError: Use Absolute Import or Modify Path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))  
from Follow_up import send_followup_email  # Import follow-up function

# 🔹 Google Sheets API Credentials
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# 🔹 Google Sheets Configuration
SPREADSHEET_ID = "1jSpYf7iEZ7HnYf4Ju60dftO3DBGBesfxn6GwJ3jpRVc"
SHEET_NAME = "Emails"

# 🔹 Email Configuration
SMTP_SERVER = "smtp-auth.iitb.ac.in"
SMTP_PORT = 587
SENDER_EMAIL = "jay.arora@iitb.ac.in"
ACCESS_TOKEN = "a7b43e5545d0be6a747e03dd91ff6edf"  # Use your generated app password

# 🔹 PDF Attachment
PDF_PATH = "Jay_Arora_Resume.pdf"  # Update with your actual PDF file path

# 🔹 Authenticate with Google Sheets API
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# 🔹 Function to Fetch Data from Google Sheets
def fetch_google_sheet_data():
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# 🔹 Function to Check for Follow-Ups (`R1`, `R2`, `R3`)
def check_followup_emails(df):
    today_date = datetime.now().date()
    r1_followup_list = []
    r2_followup_list = []
    r3_followup_list = []

    for index, row in df.iterrows():
        try:
            # Convert dates to datetime objects
            mail_sent_date = datetime.strptime(row["Mail_sent_on"], "%d-%m-%y").date()
            r1_sent_date = datetime.strptime(row["R1_sent_on"], "%d-%m-%y").date() if row["R1_sent_on"] else None
            r2_sent_date = datetime.strptime(row["R2_sent_on"], "%d-%m-%y").date() if row["R2_sent_on"] else None

            # Check for R1 Follow-up
            if (today_date - mail_sent_date).days >= 5 and row["Status"] == "Mail sent":
                r1_followup_list.append({
                    "index": index,
                    "email": row["email"],
                    "first_name": row["first_name"],
                    "message_id": row["message_id"]
                })

            # Check for R2 Follow-up
            if r1_sent_date and (today_date - r1_sent_date).days >= 5 and row["Status"] == "R1 sent":
                r2_followup_list.append({
                    "index": index,
                    "email": row["email"],
                    "first_name": row["first_name"],
                    "message_id": row["message_id"]
                })
            
            # Check for R3 Follow-up
            if r2_sent_date and (today_date - r2_sent_date).days >= 5 and row["Status"] == "R2 sent":
                r3_followup_list.append({
                    "index": index,
                    "email": row["email"],
                    "first_name": row["first_name"],
                    "message_id": row["message_id"]
                })

        except ValueError:
            print(f"❌ Skipping invalid date format for {row['email']}")

    return r1_followup_list, r2_followup_list, r3_followup_list

# 🔹 Unique Follow-Up Email Templates (Editable)
FOLLOWUP_TEMPLATES = {
    "R1": """\
    <html>
    <body style="color: black;">
        <p>Dear {first_name},</p>
        <p>I wanted to quickly follow up on my previous email regarding potential opportunities at your company.</p>
        <p>Would love to connect and discuss any potential roles that align with my experience.</p>
        <p>Looking forward to hearing from you.</p>
        <p>Best Regards,<br>Jay Arora<br>+91 9784835663</p>
    </body>
    </html>
    """,
    "R2": """\
    <html>
    <body style="color: black;">
        <p>Dear {first_name},</p>
        <p>Just wanted to check in again to see if you had a chance to review my previous email.</p>
        <p>I'm highly interested in opportunities within your team and would appreciate any updates.</p>
        <p>Please let me know if there's a good time to connect.</p>
        <p>Best Regards,<br>Jay Arora<br>+91 9784835663</p>
    </body>
    </html>
    """,
    "R3": """\
    <html>
    <body style="color: black;">
        <p>Dear {first_name},</p>
        <p>I hope you're doing well! This will be my final follow-up regarding my interest in opportunities at your company.</p>
        <p>If you’re interested, I’d love to connect. Otherwise, I completely understand and appreciate your time.</p>
        <p>Feel free to reach out in the future if there's an opportunity that fits my skillset.</p>
        <p>Best Regards,<br>Jay Arora<br>+91 9784835663</p>
    </body>
    </html>
    """
}

# 🔹 Function to Send Follow-Up Email with PDF (Ensuring Black Text & Different Content)
def send_followup_with_pdf(email, first_name, message_id, followup_type):
    try:
        subject = "Re: Regarding Full-time Opportunities"
        body = FOLLOWUP_TEMPLATES[followup_type].format(first_name=first_name)

        # Create Email Message
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = email
        msg["Subject"] = subject
        msg["In-Reply-To"] = message_id.strip()  # Threading
        msg["References"] = message_id.strip()  # Maintain thread

        msg.attach(MIMEText(body, "html"))

        # Attach PDF file
        if os.path.exists(PDF_PATH):
            with open(PDF_PATH, "rb") as attachment:
                pdf_attachment = MIMEApplication(attachment.read(), _subtype="pdf")
                pdf_attachment.add_header("Content-Disposition", f"attachment; filename={os.path.basename(PDF_PATH)}")
                msg.attach(pdf_attachment)
        else:
            print(f"⚠️ Warning: PDF file {PDF_PATH} not found. Email will be sent without an attachment.")

        # Connect to SMTP Server and Send Email
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, ACCESS_TOKEN)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())

        print(f"✅ {followup_type} Follow-up email sent to {email} (Threaded)")

    except Exception as e:
        print(f"❌ Failed to send {followup_type} follow-up email to {email}: {e}")

# 🔹 Function to Update Follow-Up Status in Google Sheets
def update_followup_status(followup_list, status_column, date_column, new_status):
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    today_date = datetime.now().strftime("%d-%m-%y")  # 🔹 Format: DD-MM-YY

    for followup in followup_list:
        row_index = followup["index"] + 2  # Adjust for 0-based index
        sheet.update_cell(row_index, status_column, new_status)
        sheet.update_cell(row_index, date_column, today_date)

# 🔹 Main Execution
def main():
    df = fetch_google_sheet_data()
    r1_followup_list, r2_followup_list, r3_followup_list = check_followup_emails(df)

    for followup in r1_followup_list:
        send_followup_with_pdf(followup["email"], followup["first_name"], followup["message_id"], "R1")
    update_followup_status(r1_followup_list, 6, 7, "R1 sent")

    for followup in r2_followup_list:
        send_followup_with_pdf(followup["email"], followup["first_name"], followup["message_id"], "R2")
    update_followup_status(r2_followup_list, 6, 8, "R2 sent")

    for followup in r3_followup_list:
        send_followup_with_pdf(followup["email"], followup["first_name"], followup["message_id"], "R3")
    update_followup_status(r3_followup_list, 6, 9, "R3 sent")

if __name__ == "__main__":
    main()
