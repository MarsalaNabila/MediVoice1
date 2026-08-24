import sqlite3
import pandas as pd
from datetime import datetime
import json
import smtplib
from email.mime.text import MIMEText

def get_email_config():
    return {
        "host": "smtp.gmail.com",
        "port": 587,
        "user": "n7141072@gmail.com",
        "password": "icswxictwfvjslof",
        "sender": "n7141072@gmail.com",
        "use_tls": True
    }

def send_email_notification(recipients, subject, body):
    recipients = [r.strip() for r in recipients if r and r.strip()]
    if not recipients:
        print("No recipients provided")
        return False, []

    config = get_email_config()
    if not config:
        print("Email config not available")
        return False, []

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = config["sender"]
    msg["To"] = ", ".join(recipients)

    try:
        if config["use_tls"]:
            server = smtplib.SMTP(config["host"], config["port"])
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(config["host"], config["port"])
        server.login(config["user"], config["password"])
        server.sendmail(config["sender"], recipients, msg.as_string())
        server.quit()
        return True, recipients
    except Exception as e:
        print(f"Email send error: {e}")
        return False, []

def get_user_email(conn, user_id):
    try:
        row = conn.execute("SELECT email FROM users WHERE username=?", (user_id,))
        record = row.fetchone()
    except sqlite3.Error:
        return None
    return record[0] if record and record[0] else None

def resolve_inventory_recipient_emails(row, user_email, family_lookup):
    try:
        notify_config = json.loads(row.get("notify_member_ids", "{}"))
    except:
        notify_config = {}
    
    member_ids = notify_config.get("members", [])
    include_self = notify_config.get("include_self", False)
    
    recipients = []
    if include_self and user_email:
        recipients.append(user_email)
    
    for mid in member_ids:
        info = family_lookup.get(mid)
        if info and info.get("email"):
            recipients.append(info["email"])
    
    return list(set(recipients))  # Remove duplicates

# Test the notification worker logic
conn = sqlite3.connect("medicine.db")
user_id = "Nabila"

print("=== TESTING NOTIFICATION WORKER ===")

# Get family lookup
family_df = pd.read_sql_query(
    "SELECT id, member_name, email FROM family_members WHERE user_id=?",
    conn,
    params=(user_id,)
)
family_lookup = {
    row["id"]: {"name": row["member_name"], "email": row["email"]}
    for _, row in family_df.iterrows()
}

user_email = get_user_email(conn, user_id)
print(f"User email: {user_email}")
print(f"Family lookup: {family_lookup}")

# Check appointments
now = datetime.now()
print(f"Current time: {now}")

appts = pd.read_sql_query(
    "SELECT * FROM appointments WHERE user_id=? AND (email_notified=0 OR voice_notified=0)",
    conn,
    params=(user_id,)
)

print(f"Found {len(appts)} appointments with pending notifications")

for _, a in appts.iterrows():
    try:
        ap_dt = datetime.strptime(f"{a['date']} {a['time']}", "%Y-%m-%d %H:%M")
        diff = (ap_dt - now).total_seconds()
        print(f"\nAppointment: {a['doctor_name']} at {a['date']} {a['time']}")
        print(f"Time difference: {diff:.0f} seconds")
        
        # Check if it should fire (within 10 seconds after appointment time)
        if -10 <= diff <= 0:
            print("-> SHOULD FIRE NOW!")
            
            # Test email notification
            if not a.get("email_notified"):
                recipients = resolve_inventory_recipient_emails(a, user_email, family_lookup)
                if not recipients and user_email:
                    recipients = [user_email]
                
                print(f"Recipients: {recipients}")
                
                if recipients:
                    subject = f"Upcoming appointment: {a['doctor_name']} on {a['date']} at {a['time']}"
                    body = f"Hi,\n\nYou have an upcoming appointment with {a['doctor_name']} at {a.get('hospital', '')} on {a['date']} at {a['time']}. Notes: {a.get('notes', '')}\n\n- MediVoice"
                    
                    print("Sending email...")
                    sent, sent_to = send_email_notification(recipients, subject, body)
                    if sent:
                        print(f"Email sent successfully to: {sent_to}")
                        # Update database
                        conn.execute("UPDATE appointments SET email_notified=1 WHERE id=?", (a["id"],))
                        conn.commit()
                    else:
                        print("Email failed to send")
                else:
                    print("No recipients found")
            else:
                print("Email already sent")
        else:
            if diff > 0:
                print(f"-> Future appointment ({diff/60:.1f} minutes from now)")
            else:
                print(f"-> Past appointment ({-diff/60:.1f} minutes ago)")
                
    except Exception as e:
        print(f"Error processing appointment: {e}")

conn.close()
print("\n=== TEST COMPLETE ===")