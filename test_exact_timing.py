import sqlite3
import json
from datetime import datetime, timedelta

def create_exact_time_appointment():
    """Create an appointment for exactly 1 minute from now"""
    conn = sqlite3.connect("medicine.db")
    
    # Get current time and add exactly 1 minute
    now = datetime.now()
    appointment_time = now + timedelta(minutes=1)
    
    # Round to nearest minute for cleaner display
    appointment_time = appointment_time.replace(second=0, microsecond=0)
    
    # Insert appointment
    conn.execute("""
        INSERT INTO appointments(user_id, doctor_name, hospital, date, time, notes, notify_member_ids, email_notified, voice_notified)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
    """, (
        "Nabila",  # Use your actual username
        "Dr. Exact Time Test",
        "Test Hospital",
        appointment_time.strftime("%Y-%m-%d"),
        appointment_time.strftime("%H:%M"),
        "Test appointment for exact timing",
        json.dumps({"members": [], "include_self": True})
    ))
    conn.commit()
    conn.close()
    
    print(f"Created appointment for EXACTLY {appointment_time.strftime('%H:%M:%S')}")
    print(f"Current time: {now.strftime('%H:%M:%S')}")
    print(f"Alert will trigger at: {appointment_time.strftime('%H:%M:%S')}")
    print("\nMake sure MediVoice app is running and you're logged in!")
    print("The alert should trigger exactly at the appointment time, not before.")

def cleanup_test_appointments():
    """Remove test appointments"""
    conn = sqlite3.connect("medicine.db")
    conn.execute("DELETE FROM appointments WHERE doctor_name LIKE '%Test%'")
    conn.commit()
    conn.close()
    print("Cleaned up test appointments")

if __name__ == "__main__":
    print("=== Exact Timing Test ===")
    print("1. Cleaning up old test appointments...")
    cleanup_test_appointments()
    
    print("\n2. Creating new appointment for exact timing test...")
    create_exact_time_appointment()
    
    print("\n3. Now run your MediVoice app and wait for the exact time!")
    print("   The notification should trigger precisely at the appointment time.")