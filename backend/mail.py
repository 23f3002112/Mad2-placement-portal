import os
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

# Defaulting to MailHog settings
SMTP_SERVER = os.environ.get("SMTP_SERVER", "localhost")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "1025"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SENDER = os.environ.get("MAIL_SENDER", "noreply@jobfinder.com")


def send_email(to_address, subject, message, content="html", attachment_file=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = to_address
    msg["Subject"] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    if attachment_file and os.path.exists(attachment_file):
        with open(attachment_file, "rb") as file_obj:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file_obj.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(attachment_file)}"')
        msg.attach(part)

    try:
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        if SMTP_USERNAME:
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.send_message(msg)
        smtp.quit()
        print(f"[MAILHOG] Sent email to {to_address} via {SMTP_SERVER}:{SMTP_PORT}")
        return True
    except Exception as e:
        print(f"[MAILHOG ERROR] Failed to send email to {to_address}: {e}")
        return False
