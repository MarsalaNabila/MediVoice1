import sqlite3
from datetime import datetime, timedelta
import json

# Connect to database
conn = sqlite3.connect("medicine.db")

# Create an appointment for 1 minute from now
now = datetime.now()
test_time = now + timedelta(minutes=1)
date_str = test_time.strftime("%Y-%m-%d")
time_str = test_time.strftime("%H:%M")

print(f"Creating test appointment for: {date_str} at {time_str}")

# Get family member IDs for notification
cursor = conn.cursor()
cursor.execute("SELECT id FROM family_members WHERE user_id='Nabila' AND email IS NOT NULL")
family_ids = [row[0] for row in cursor.fetchall()]

# Create notification config (include self + family members)
notify_config = json.dumps({
    "members": family_ids,
    "include_self": True
})

# Insert the appointment
cursor.execute("""
    INSERT INTO appointments(user_id, doctor_name, hospital, date, time, notes, notify_member_ids, email_notified, voice_notified)
    VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
""", (
    "Nabila",
    "Dr. Voice Test",
    "Language Test Hospital",
    date_str,
    time_str,
    "Test appointment to verify voice language setting works correctly",
    notify_config
))

conn.commit()
print("Test appointment created successfully!")
print("This appointment will test if voice alerts use the language setting from the app.")
print("Make sure you're logged in as 'Nabila' in the MediVoice app.")
print("Change the 'Voice Alert Language' setting in the sidebar to test different languages.")

conn.close()