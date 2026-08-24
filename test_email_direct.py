import smtplib
from email.mime.text import MIMEText

# Test email configuration directly
config = {
    "host": "smtp.gmail.com",
    "port": 587,
    "user": "n7141072@gmail.com",
    "password": "icswxictwfvjslof",
    "sender": "n7141072@gmail.com",
    "use_tls": True
}

recipients = ["marsalauddinnabila@gmail.com"]
subject = "MediVoice Test - Doctor Appointment Reminder"
body = """Hi,

This is a test email from MediVoice to verify that appointment reminders are working correctly.

You have a test appointment with Dr. Test Email at Test Hospital.

- MediVoice"""

print("Testing email configuration...")
print(f"SMTP Host: {config['host']}")
print(f"SMTP Port: {config['port']}")
print(f"SMTP User: {config['user']}")
print(f"Recipients: {recipients}")

try:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = config["sender"]
    msg["To"] = ", ".join(recipients)

    if config["use_tls"]:
        server = smtplib.SMTP(config["host"], config["port"])
        server.starttls()
    else:
        server = smtplib.SMTP_SSL(config["host"], config["port"])
    
    server.login(config["user"], config["password"])
    server.sendmail(config["sender"], recipients, msg.as_string())
    server.quit()
    
    print("SUCCESS: Email sent successfully!")
    print("Check your inbox for the test email.")
    
except Exception as e:
    print(f"ERROR: Email failed: {e}")