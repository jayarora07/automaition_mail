# Email Outreach Automation

A Python-based workflow for sending personalized outreach emails, scheduling up to three follow-ups, tracking campaign progress in Google Sheets, and detecting replies through IMAP.

> [!WARNING]
> This repository is currently intended for private use. It has previously contained email and Google service-account credentials. Remove credentials from the complete Git history and rotate the affected keys before making the repository public.

## What it does

- Reads recipient names and email addresses from Google Sheets.
- Sends a personalized first email with a PDF resume attached.
- Records the generated message ID, sent date, and delivery status in the sheet.
- Sends up to three follow-ups at five-day intervals.
- Keeps follow-ups in the original email thread using `In-Reply-To` and `References` headers.
- Checks the inbox for replies and marks matching recipients as `Replied`.

## Project structure

| File | Purpose |
| --- | --- |
| `First_Mail.py` | Sends the initial personalized email and records its metadata in Google Sheets. |
| `Follow_up.py` | Contains a reusable helper for sending a threaded follow-up email. |
| `Follow_ups.py` | Selects recipients eligible for R1, R2, or R3 follow-ups, sends the messages, and updates the sheet. |
| `Check_replies.py` | Reads recent inbox messages through IMAP and marks matching contacts as replied. |
| `requirements.txt` | Lists the Python packages required by the scripts. |
| `Jay_Arora_Resume.pdf` | Resume attached to outgoing messages. |

## How the workflow fits together

1. Add prospects to the `Emails` worksheet.
2. Run `First_Mail.py` to send the initial outreach emails.
3. Run `Follow_ups.py` periodically to send eligible follow-ups.
4. Run `Check_replies.py` to find responses and update their status.

Google Sheets acts as the campaign tracker and source of truth throughout the workflow.

## Google Sheet structure

Create a worksheet named `Emails` with these columns:

| Column | Description |
| --- | --- |
| `email` | Recipient's email address. |
| `first_name` | Recipient's first name for personalization. |
| `message_id` | Message ID generated for the first email. |
| `Mail_sent_on` | Initial email date in `DD-MM-YY` format. |
| `Status` | Campaign state, such as `Mail sent`, `R1 sent`, `R2 sent`, `R3 sent`, or `Replied`. |
| `R1_sent_on` | First follow-up date in `DD-MM-YY` format. |
| `R2_sent_on` | Second follow-up date in `DD-MM-YY` format. |
| `R3_sent_on` | Third follow-up date in `DD-MM-YY` format. |

Share the spreadsheet with the service account's `client_email` so the scripts can read and update it.

## Requirements

- Python 3.9 or newer
- A Google Cloud service account with Google Sheets API access
- A Google Sheet containing the columns listed above
- SMTP and IMAP access to the sender's email account
- A PDF attachment at the path configured by `PDF_PATH`

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/jayarora07/automaition_mail.git
cd automaition_mail
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\activate
```

## Configuration

The current scripts use configuration constants near the top of each file. Before running them, configure:

- `SERVICE_ACCOUNT_FILE`
- `SPREADSHEET_ID`
- `SHEET_NAME`
- `SMTP_SERVER` and `SMTP_PORT`
- `IMAP_SERVER` and `IMAP_PORT`
- `SENDER_EMAIL` or `EMAIL_ID`
- `ACCESS_TOKEN`
- `PDF_PATH`

Place the Google service-account key at the configured local path. Never commit that file, email tokens, passwords, or other credentials.

## Usage

Send the initial outreach emails:

```bash
python First_Mail.py
```

Send follow-ups that have become eligible:

```bash
python Follow_ups.py
```

Check the inbox for replies and update the sheet:

```bash
python Check_replies.py
```

These commands send real emails and update the connected Google Sheet. Test with a small recipient list before running a full campaign.

## Follow-up schedule

The automation uses the following default sequence:

- **R1:** Five days after the first email if the status is `Mail sent`.
- **R2:** Five days after R1 if the status is `R1 sent`.
- **R3:** Five days after R2 if the status is `R2 sent`.

Each follow-up uses the original message ID so compatible email clients display it in the same conversation.

## Important security notes

- Keep `credentials.json`, tokens, passwords, virtual environments, and `__pycache__` out of Git.
- Load secrets from environment variables or a local `.env` file rather than source-code constants.
- Revoke and replace any credential that has ever been committed.
- Rewrite the repository history before changing a repository containing secrets from private to public.
- Avoid disabling TLS certificate and hostname verification in production.

## Responsible use

Use this project only for legitimate, targeted outreach. Follow applicable privacy, anti-spam, and email-provider rules, and provide recipients with a clear way to opt out.
