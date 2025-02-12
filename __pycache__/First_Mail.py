import gspread
import pandas as pd
import smtplib
import ssl
from google.oauth2.service_account import Credentials
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime  # 🔹 Import datetime for date formatting
import os

# 🔹 Load Google Sheets API credentials
SERVICE_ACCOUNT_FILE = "credentials.json"  # Path to your downloaded JSON key file
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# 🔹 Authenticate with Google Sheets API
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# 🔹 Google Sheet ID and Sheet Name
SPREADSHEET_ID = "1jSpYf7iEZ7HnYf4Ju60dftO3DBGBesfxn6GwJ3jpRVc"  # Get this from the Google Sheet URL
SHEET_NAME = "12th Feb"  # Change this to your actual sheet name

# 🔹 Fetch data from Google Sheets
def fetch_google_sheet_data():
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    
    # Expected headers to avoid duplicate column issues
    expected_headers = ["email", "first_name", "message_id", "Mail_sent_on", "Status"]  # Added "Status"
    
    data = sheet.get_all_records(expected_headers=expected_headers)  # Ensure correct headers
    return pd.DataFrame(data)  # Convert to Pandas DataFrame

# 🔹 Fetch the latest data
df = fetch_google_sheet_data()

# 🔹 Email credentials
SMTP_SERVER = "smtp-auth.iitb.ac.in"
SMTP_PORT = 587
SENDER_EMAIL = "jay.arora@iitb.ac.in"
ACCESS_TOKEN = "e79c19c2b430789e51035d72dc59a25b"  # Use your generated app password  

# 🔹 PDF Attachment (Resume)
PDF_PATH = "Jay_Arora_Resume.pdf"

# 🔹 Email Subject & Template (With Bold Formatting)
EMAIL_SUBJECT = "Regarding Full-time Opportunities"
EMAIL_TEMPLATE = """\
<html>
  <body style="color: black;">
    
    <p>Dear {first_name},</p>

    <p>Warm Greetings!</p>

    <p>I hope this email finds you well.</p>

    <p>
      I am Jay Arora, a final-year undergraduate at IIT Bombay, graduating in 2025.
      I am reaching out to explore potential full-time opportunities in <b>Product Management</b> or 
      <b>Founder’s Office roles</b> within your esteemed organization.
    </p>

    <p>Here’s a brief overview of my professional experiences:</p>

    <ul>
      <li><b>Zeno Health (Product Management Intern)</b>: Led app development to enhance store operations and user engagement.</li>
      <li><b>Nova Benefits (Business Analyst Intern)</b>: Automated workflows and improved client engagement strategies.</li>
      <li><b>NeuralThread (Business Development Intern)</b>: Designed sales strategies and expanded client portfolios.</li>
    </ul>

    <p>Talking about my college journey:</p>

    <ul>
      <li><b>Leadership</b>: Led SARC’s 75+ member team and mentored students as a DAMP-ARP mentor.</li>
      <li><b>Projects</b>: Developed a start-up idea in <b>Second Bite</b> to tackle food wastage and devised strategies in the <b>Indian Case Challenge</b> for user engagement and retention.</li>
      <li><b>Extracurriculars & Achievements</b>: Volunteered for social initiatives like teaching underprivileged students and received the <b>Institute Academic Award</b> for securing Department Rank 1.</li>
    </ul>

    <p>
      I have attached my resume and would be grateful for an opportunity to discuss relevant roles or connect with the appropriate team.
    </p>

    <p>
      For a more detailed overview of my work and experiences, please feel free to explore my documents  
      <a href="https://drive.google.com/drive/folders/193HHf0hJZ5c-Ah8B3pDgtzQZ1vuO3VvE?usp=sharing" target="_blank">
        here
      </a>.
    </p>

    <p>
      Please feel free to contact me at <b>jay.arora@iitb.ac.in</b> or +91 9784835663.
    </p>

    <p>Thank you for your time and consideration.</p>

    <p>Best Regards,<br>
    Jay Arora<br>
    +91 9784835663</p>

  </body>
</html>

"""

# 🔹 Function to Send Emails with Attachments and Update Google Sheet
def send_email(receiver_email, first_name, row_index):
    try:
        # Create Email Message
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = EMAIL_SUBJECT

        # 🔹 Generate a unique Message-ID
        message_id = f"<{row_index}.{int(datetime.now().timestamp())}@iitb.ac.in>"
        msg["Message-ID"] = message_id  # Attach Message-ID to email

        # Personalize the message
        body = EMAIL_TEMPLATE.format(first_name=first_name)
        msg.attach(MIMEText(body, "html"))  # Use HTML format

        # Attach PDF file (Resume)
        if os.path.exists(PDF_PATH):
            with open(PDF_PATH, "rb") as attachment:
                pdf_attachment = MIMEApplication(attachment.read(), _subtype="pdf")
                pdf_attachment.add_header(
                    "Content-Disposition", f"attachment; filename={os.path.basename(PDF_PATH)}"
                )
                msg.attach(pdf_attachment)
        else:
            print(f"⚠️ Warning: PDF file {PDF_PATH} not found. Email will be sent without an attachment.")

        # Connect to SMTP Server and Send Email
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)  # Secure the connection
            server.login(SENDER_EMAIL, ACCESS_TOKEN)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())

        print(f"✅ Email sent to {receiver_email} (Message-ID: {message_id})")

        # 🔹 Store the Message-ID, Email Sent Date, and Status in Google Sheets
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
        today_date = datetime.now().strftime("%d-%m-%y")  # 🔹 Format: DD-MM-YY
        sheet.update_cell(row_index + 2, 4, message_id)  # Column D (4th column) for "message_id"
        sheet.update_cell(row_index + 2, 5, today_date)  # Column E (5th column) for "Mail_sent_on"
        sheet.update_cell(row_index + 2, 6, "Mail sent")  # Column F (6th column) for "Status"

    except Exception as e:
        print(f"❌ Failed to send email to {receiver_email}: {e}")


# 🔹 Loop Through Recipients and Send Emails
for index, row in df.iterrows():
    send_email(row["email"], row["first_name"], index)  # ✅ Pass 'index' as row_index
