import sqlite3
import json
from datetime import datetime, timedelta
from voice_alert import speak

def test_appointment_alert():
    # Create a test appointment for 1 minute from now
    conn = sqlite3.connect("medicine.db")
    
    # Get current time and add 1 minute
    now = datetime.now()
    test_time = now + timedelta(minutes=1)
    
    # Insert test appointment
    conn.execute("""
        INSERT INTO appointments(user_id, doctor_name, hospital, date, time, notes, notify_member_ids, email_notified, voice_notified)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
    """, (
        "test_user",
        "Dr. Test",
        "Test Hospital", 
        test_time.strftime("%Y-%m-%d"),
        test_time.strftime("%H:%M"),
        "Test appointment",
        json.dumps({"members": [], "include_self": True})
    ))
    conn.commit()
    
    print(f"Created test appointment for {test_time.strftime('%Y-%m-%d %H:%M')}")
    print("Waiting for alert...")
    
    # Wait and check for the appointment
    import time
    while True:
        current_time = datetime.now()
        
        # Check if it's time for the appointment (within 30 seconds)
        diff = (test_time - current_time).total_seconds()
        
        if -30 <= diff <= 30:
            print(f"Time for appointment! Playing alert...")
            
            # Play voice alert
            speak(f"You have a doctor appointment with Dr. Test at {test_time.strftime('%H:%M')}", "en")
            
            # Send email (if configured)
            print("Email would be sent here if SMTP is configured")
            
            break
        
        print(f"Waiting... {diff:.0f} seconds until appointment")
        time.sleep(5)
    
    # Clean up
    conn.execute("DELETE FROM appointments WHERE doctor_name='Dr. Test'")
    conn.commit()
    conn.close()
    
    print("Test completed!")

if __name__ == "__main__":
    test_appointment_alert()