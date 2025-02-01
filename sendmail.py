import os
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define your SMTP server and credentials
SMTP_SERVER = "smtp-auth.iitb.ac.in"
SMTP_PORT = 587
SMTP_USERNAME = "21b030019@iitb.ac.in"
SMTP_PASSWORD = "cbddfc8142391ab00225e11a673e228c"

# Create a list to store email addresses that couldn't be sent successfully
leftUsers = []

def send_welcome_mail(userName, userEmail, Employee_Impact_Moments, user_login_percentage, hours_saved, value_created, incurred_claims_ratio, claims_settled, claims_settled_amount, lives_covered_as_of_date, net_premium_added_from_inception, tickets_raised, avg_first_response_time, avg_resolution_time, participation_in_engagement_sessions, teleconsultation_utilisation, hra_utilisation, health_checks_utilisation):
    subject = "my intern"
    # Create the MIME message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = userEmail

    # Create the HTML email content
    html_content =f'''
 <!DOCTYPE html>
<html lang="en">
<head>
  <title>Your Monthly Health & Wellness Roundup: November, 2023 Edition</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; margin: 20px;">

  <!-- Header with logos -->
  <div style="display:flex; flex-direction:row; justify-content:space-between; margin:20px; ">
    <img width="30%" src="https://drive.google.com/thumbnail?id=1QLh02S4y-KINSmMovV02SyqR3E9yGBUq" alt="">
    <img width="30%" src="https://drive.google.com/thumbnail?id=1QLh02S4y-KINSmMovV02SyqR3E9yGBUq" alt="">
  </div>

  <!-- Main Title -->
  <div style="font-size: 18px; font-weight:bolder; text-align: center; background-color: #e0e0e0;">
    Your Monthly Health & Wellness Roundup: November, 2023 Edition
  </div>

  <!-- Overall Summary -->
  <h2 style="font-size: 24px; text-align: center; margin-top: 20px; border-bottom: 2px solid #3333337b; font-family: 'cursive'; font-style: italic;">Overall Summary</h2>
  <ul style="list-style-type: none; margin: 0; padding: 0; display: flex; width: 100%;">
    <li style="display: flex; flex: 1; text-align: center; margin-left: 50px; padding: 0 20px; flex-direction: column;">
      <span>{Employee_Impact_Moments}</span>
      <span>% # Employee Impact Moments</span>
    </li>

    <li style="flex: 1; margin-left: 10px; display: flex; flex-direction:column; text-align: center;">
      <span>{user_login_percentage}</span>
      <span>% User Login</span>
    </li>
    
    <li style="flex: 1; margin-left: 10px; display: flex; flex-direction:column; text-align: center;">
      <span>{hours_saved}</span>
      <span># Hours Saved</span>
    </li>
    
    <li style="flex: 1; margin-left: 10px; display: flex; flex-direction:column; text-align: center;">
      <span>{value_created}</span>
      <span>Value Created</span>
    </li>
  </ul>

  <!-- Health Insurance: Claims -->
  <h2 style="font-size: 24px; text-align: center; margin-top: 20px; border-bottom: 2px solid #3333337b; font-family: 'cursive'; font-style: italic;">Health Insurance: Claims</h2>
  <ul style="list-style-type: none; margin: 0; padding: 0; display: flex;">
    <li style="display: flex; flex: 1; text-align: center; flex-direction: column;">
      <span>{incurred_claims_ratio}</span>
      <span>Incurred Amount</span>
    </li>
    <li style="flex: 1; display:flex; flex-direction:column; text-align:center;">
      <span>{claims_settled}</span>
      <span># Claims Settled</span>
    </li>
    <li style="flex: 1; display:flex; flex-direction:column; text-align:center;">
      <span>{claims_settled_amount}</span>
      <span>Claims Settled Amount</span>
    </li>
  </ul>

  <!-- Health Insurance: Endorsements -->
  <h2 style="font-size: 24px; text-align: center; margin-top: 20px; border-bottom: 2px solid #3333337b; font-family: 'cursive'; font-style: italic;">Health Insurance: Endorsements</h2>
  <ul style="list-style-type: none; margin: 0; padding: 0; display: flex; width: 100%;">
    <li style="flex: 1; display:flex; flex-direction:column; text-align:center;">
      <span>{lives_covered_as_of_date}</span>
      <span># Lives Covered As of Date</span>
    </li>
    <li style="flex: 1; display:flex; flex-direction:column; text-align:center;">
      <span>{net_premium_added_from_inception}</span>
      <span>Net Premium Added from Inception</span>
    </li>
  </ul>

  <!-- Health Insurance: Customer Support -->
  <h2 style="font-size: 24px; text-align: center; margin-top: 20px; border-bottom: 2px solid #3333337b; font-family: 'cursive'; font-style: italic;">Health Insurance: Customer Support</h2>
  <ul style="list-style-type: none; margin: 0; padding: 0; display: flex; width: 100%;">
    <li style="display: flex; flex: 1; text-align: center; flex-direction: column;">
      <span>{tickets_raised}</span>
      <span># Tickets Raised</span>
    </li>
    <li style="flex: 1; display:flex; flex-direction:column; text-align:center;">
      <span>{avg_first_response_time}</span>
      <span># Avg First Response Time</span>
    </li>
    <li style="flex: 1; display:flex; flex-direction:column; text-align:center;">
      <span>{avg_resolution_time}</span>
      <span># Avg Resolution Time</span>
    </li>
  </ul>

  <!-- Wellness Updates -->
  <h2 style="font-size: 24px; text-align: center; margin-top: 20px; border-bottom: 2px solid #3333337b; font-family: 'cursive'; font-style: italic;">Wellness Updates</h2>
  <ul style="list-style-type: none; margin: 0; padding: 0; display: flex; width: 100%;">
    <li style="display: flex; flex: 1; text-align: center; margin-left: 50px; padding: 0 20px; flex-direction: column;">
      <span>{participation_in_engagement_sessions}</span>
      <span>% Participation in Engagement Sessions</span>
    </li>
    <li style="flex: 1; margin-left: 10px; display: flex; flex-direction:column; text-align: center;">
      <span>{teleconsultation_utilisation}</span>
      <span>% Teleconsultation Utilization</span>
    </li>
    <li style="flex: 1; margin-left: 10px; display: flex; flex-direction:column; text-align: center;">
      <span>{hra_utilisation}</span>
      <span>% HRA Utilization</span>
    </li>
  </ul>
  
  <!-- Some Popular Picks of HRs -->
<h2 style="font-size: 24px; text-align: center; margin-top: 20px; border-bottom: 2px solid #3333337b; font-family: 'cursive'; font-style: italic;">
  <img style="margin-bottom: -0.3%" width="2%" src="https://drive.google.com/thumbnail?id=1QKIaLVZapxqhJs-K8UdeZAT6yd9UiKdt" alt="">
  Some Popular Picks of HRs
  <img style="margin-bottom: -0.3%" width="2%" src="https://drive.google.com/thumbnail?id=1QKIaLVZapxqhJs-K8UdeZAT6yd9UiKdt" alt="">
</h2>
<div style="display: flex; justify-content: space-around;">

  <!-- Group 1: Some Popular Picks of HRs - Insurance -->
  <div>
    <ul style="list-style-type: none; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center;">
      <li style="margin: 0; padding: 0 20px;"><strong>Insurance</strong></li>

      <a href="#">
        <li style="margin: 0; padding: 0 20px; color: blue;">Group Personal Accident Insurance</li>
      </a>
      <a href="#">
        <li style="margin: 0; padding: 0 20px; color: blue;">Group Term Life Insurance</li>
      </a>
      <a href="#">
        <li style="margin: 0; padding: 0 20px; color: blue;">Parental Insurance</li>
      </a>
    </ul>
  </div>

  <!-- Group 2: Some Popular Picks of HRs - Wellness -->
  <div>
    <ul style="list-style-type: none; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center;">
      <li style="margin: 0; padding: 0 20px;"><strong>Wellness</strong></li>
      <a href="">
        <li style="margin: 0; padding: 0 20px; color: blue;">Annual Health Check-ups</li>
      </a>
      <a href="">
        <li style="margin: 0; padding: 0 20px; color: blue;">Telehealth Consultations</li>
      </a>
      <a href="">
        <li style="margin: 0; padding: 0 20px; color: blue;">Gym Subscription</li>
      </a>
      <a href="">
        <li style="margin: 0; padding: 0 20px; color: blue;">Mental Wellness Insurance</li>
      </a>
    </ul>
  </div>

</div>


  <!-- Placeholder for extended discussion link -->
  <p style=" margin-top: 30px; text-align: center; margin:10px">We hope to enhance your experience further and work together on many new offerings. If you want to have an extended discussion on any of the above offerings with your Key Account Manager, please click on this <a href="#">LINK.</a></p>

  <!-- Footer Section -->
  <div style="background-color: #051C22; width: 100%; padding:10%; display:flex; flex-direction:column; justify-content:center; align-items:center">
    <div style="color: gray;">
      Best Experienced On
    </div>
    <div style="display: flex; flex-direction:row; margin:2%">
      <a href="#">
        <img src="https://drive.google.com/thumbnail?id=1QSMs_mj8FlFBY8muujxiluJdGHpRW1DI" alt="">
      </a>
      <a href="#">
        <img src="https://drive.google.com/thumbnail?id=1QUBBOacHfRnt2Hmpf4kbzneqzlAaTvQc" alt="">
      </a>
    </div>
    <div style="color: gray;">
      You have received this mail because you are a client of Nova Benefits.
    </div>
    <img style="margin-top: 2%;" src="https://drive.google.com/thumbnail?id=1QLzJoKN2E-XDTwqjdaB6b5SS_S8-HZjd" alt="">
    <div style="color: gray; display: flex; flex-direction:row;">
      <a style="color: gray; " href="#">Careers</a> &nbsp; | &nbsp;<a style="color: gray; " href="#">Terms of Use</a> &nbsp; | &nbsp;<a style="color: gray; " href="">Privacy Policy</a>
    </div>
  </div>

</body>
</html>


    '''

    # Attach the HTML content
    msg.attach(MIMEText(html_content, "html"))

    # Create an SMTP connection and send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            smtp.sendmail(SMTP_USERNAME, userEmail, msg.as_string())
    except Exception as e:
        print(f"Error sending email to {userName}: {e}")
        leftUsers.append(userName)

def mail_users():
    file_path = os.path.join(os.getcwd(), 'Automation.csv')
    with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                company_name = row["Company Name"]
                employee_impact_moments = row["Employee_Impact_Moments"]
                user_login = row["User_Login"]
                hours_saved = row["Hours_Saved"]
                value_created = row["Value_Created"]
                incurred_claims_ratio = row["Incurred_Claims_Ratio"]
                claims_settled = row["Claims_Settled"]
                claims_settled_amount = row["Claims_Settled_Amount"]
                lives_covered_as_of_date = row["Lives_Covered_As_of_Date"]
                net_premium_added_from_inception = row["Net_Premium_Added_from_Inception"]
                tickets_raised = row["Tickets_Raised"]
                avg_first_response_time = row["Avg_First_Response_Time"]
                avg_resolution_time = row["Avg_Resolution_Time"]
                participation_in_engagement_sessions = row["Participation_in_Engagement_Sessions"]
                teleconsultation_utilisation = row["Teleconsultation_Utilisation"]
                hra_utilisation = row["HRA_Utilisation"]
                health_checks_utilisation = row["Health_Checks_Utilisation"]
                user_email = row["UserEmail"]
                send_welcome_mail(userName="user", userEmail=user_email, Employee_Impact_Moments=employee_impact_moments, user_login_percentage=user_login, hours_saved=hours_saved, value_created=value_created, incurred_claims_ratio=incurred_claims_ratio, claims_settled=claims_settled, claims_settled_amount=claims_settled_amount, lives_covered_as_of_date=lives_covered_as_of_date, net_premium_added_from_inception=net_premium_added_from_inception, tickets_raised=tickets_raised, avg_first_response_time=avg_first_response_time, avg_resolution_time=avg_resolution_time, participation_in_engagement_sessions=participation_in_engagement_sessions, teleconsultation_utilisation=teleconsultation_utilisation, hra_utilisation=hra_utilisation, health_checks_utilisation=health_checks_utilisation)
            except Exception as e:
                print(f"Error sending email to {user_email}: {e}")
                leftUsers.append(user_email)

if __name__ == "__main__":
    mail_users()
    print("Emails sent successfully to recipients.")
    if leftUsers:
        print(f"Emails not sent to the following recipients: {', '.join(leftUsers)}")
