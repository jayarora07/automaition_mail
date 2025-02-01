import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import ssl

# 🔹 IMAP Credentials for IITB Webmail
IMAP_SERVER = "imap.iitb.ac.in"
IMAP_PORT = 993
EMAIL_ID = "jay.arora@iitb.ac.in"
ACCESS_TOKEN = "a7b43e5545d0be6a747e03dd91ff6edf"

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

def fetch_recent_emails(mail):
    try:
        mail.select("INBOX")
        # Calculate date 48 hours ago
        date_since = (datetime.now() - timedelta(hours=48)).strftime("%d-%b-%Y")
        query = f'(SINCE "{date_since}")'
        
        status, messages = mail.search(None, query)
        if status != "OK":
            print("❌ Error fetching emails")
            return
        
        print("\n📧 Recent emails (last 48 hours):")
        for num in messages[0].split():
            status, msg_data = mail.fetch(num, "(RFC822)")
            if status != "OK":
                continue
                
            email_body = msg_data[0][1]
            email_msg = email.message_from_bytes(email_body)
            
            # Get sender
            sender = email.utils.parseaddr(email_msg["From"])[1]
            # Get subject
            subject = email_msg["Subject"]
            if subject:
                # Decode subject if needed
                decoded_subject = decode_header(subject)[0][0]
                if isinstance(decoded_subject, bytes):
                    decoded_subject = decoded_subject.decode()
            else:
                decoded_subject = "No Subject"
                
            print(f"\nFrom: {sender}")
            print(f"Subject: {decoded_subject}")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Error while fetching emails: {e}")

def main():
    mail = connect_to_imap()
    if mail:
        fetch_recent_emails(mail)
        mail.logout()
        print("\n✅ Logged out successfully")

if __name__ == "__main__":
    main()
