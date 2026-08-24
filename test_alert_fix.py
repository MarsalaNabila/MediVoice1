#!/usr/bin/env python3
"""
Test script to verify doctor appointment alerts are working
Creates a test appointment 30 seconds in the future and simulates the notification worker
"""
import sqlite3
from datetime import datetime, timedelta
import time
import sys

# Connect to database
conn = sqlite3.connect(r'c:\MediVoice\medical_reminders.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get a test user (use user_id=1)
cursor.execute("SELECT id, email FROM users LIMIT 1")
user = cursor.fetchone()
if not user:
    print("ERROR: No users in database")
    sys.exit(1)

user_id = user['id']
user_email = user['email']
print(f"Test user: ID={user_id}, Email={user_email}")

# Create appointment 30 seconds in the future
now = datetime.now()
future_time = now + timedelta(seconds=30)

# Format for appointment
appt_date = future_time.strftime("%Y-%m-%d")
appt_time = future_time.strftime("%H:%M")

print(f"\nCreating test appointment for {appt_date} at {appt_time}")

# Insert appointment
cursor.execute("""
    INSERT INTO appointments 
    (user_id, doctor_name, date, time, email_notified, voice_notified)
    VALUES (?, ?, ?, ?, 0, 0)
""", (user_id, "Dr. Test", appt_date, appt_time))
conn.commit()

appt_id = cursor.lastrowid
print(f"Created appointment ID={appt_id}")

# Now wait and simulate the notification worker checking for alerts
print(f"\n⏳ Waiting 35 seconds to catch appointment time window...")
print("Checking every 5 seconds...\n")

for i in range(7):  # Check 7 times (35 seconds total)
    time.sleep(5)
    
    # Query the appointment to check flags
    cursor.execute("""
        SELECT email_notified, voice_notified, time FROM appointments WHERE id=?
    """, (appt_id,))
    appt = cursor.fetchone()
    
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"[{current_time}] Check #{i+1}:")
    print(f"  Appointment time: {appt['time']}")
    print(f"  Email notified: {appt['email_notified']}")
    print(f"  Voice notified: {appt['voice_notified']}")
    
    if appt['email_notified'] and appt['voice_notified']:
        print("\n✅ SUCCESS! Both email and voice alerts were sent!")
        break
    elif appt['email_notified'] or appt['voice_notified']:
        print("\n⚠️  PARTIAL: One alert sent but not both")
    else:
        print("  (still waiting...)")

print("\nTest complete.")

# Clean up
cursor.execute("DELETE FROM appointments WHERE id=?", (appt_id,))
conn.commit()
conn.close()
