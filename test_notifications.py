import sqlite3
import json
from datetime import datetime, timedelta
import sys
import os

# Add the current directory to Python path to import voice_alert
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from voice_alert import speak
    print("✓ Voice module imported successfully")
except ImportError as e:
    print(f"✗ Voice module import failed: {e}")
    speak = None

def test_email_config():
    """Test if email configuration is working"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        
        # Test SMTP connection
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("n7141072@gmail.com", "icswxictwfvjslof")
        server.quit()
        print("✓ Email configuration is working")
        return True
    except Exception as e:
        print(f"✗ Email configuration failed: {e}")
        return False

def test_voice_alert():
    """Test voice alert functionality"""
    if speak is None:
        print("✗ Voice module not available")
        return False
    
    try:
        print("Testing voice alert...")
        speak("This is a test voice alert from MediVoice", "en")
        print("✓ Voice alert test completed")
        return True
    except Exception as e:
        print(f"✗ Voice alert failed: {e}")
        return False

def create_test_appointment():
    """Create a test appointment for immediate testing"""
    conn = sqlite3.connect("medicine.db")
    
    # Create appointment for 30 seconds from now
    test_time = datetime.now() + timedelta(seconds=30)
    
    conn.execute("""
        INSERT INTO appointments(user_id, doctor_name, hospital, date, time, notes, notify_member_ids, email_notified, voice_notified)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
    """, (
        "test_user",
        "Dr. Test Alert",
        "Test Hospital",
        test_time.strftime("%Y-%m-%d"),
        test_time.strftime("%H:%M"),
        "Test appointment for notification",
        json.dumps({"members": [], "include_self": True})
    ))
    conn.commit()
    conn.close()
    
    print(f"✓ Created test appointment for {test_time.strftime('%H:%M:%S')}")
    return test_time

def cleanup_test_data():
    """Remove test appointments"""
    conn = sqlite3.connect("medicine.db")
    conn.execute("DELETE FROM appointments WHERE doctor_name LIKE 'Dr. Test%'")
    conn.commit()
    conn.close()
    print("✓ Cleaned up test data")

def main():
    print("=== MediVoice Notification System Test ===\n")
    
    # Test 1: Email configuration
    print("1. Testing email configuration...")
    email_ok = test_email_config()
    
    # Test 2: Voice alert
    print("\n2. Testing voice alert...")
    voice_ok = test_voice_alert()
    
    # Test 3: Create test appointment
    print("\n3. Creating test appointment...")
    test_time = create_test_appointment()
    
    print(f"\n4. Waiting for appointment alert at {test_time.strftime('%H:%M:%S')}...")
    print("   (The background notification worker should trigger the alert)")
    print("   Check your email and listen for voice alert!")
    
    # Wait a bit then cleanup
    import time
    time.sleep(60)  # Wait 1 minute
    
    print("\n5. Cleaning up...")
    cleanup_test_data()
    
    print("\n=== Test Summary ===")
    print(f"Email: {'✓ Working' if email_ok else '✗ Failed'}")
    print(f"Voice: {'✓ Working' if voice_ok else '✗ Failed'}")
    print("\nIf you didn't receive the appointment alert, check:")
    print("- Make sure the MediVoice app is running")
    print("- Check that you're logged in as 'test_user' or create a real appointment")
    print("- Verify email settings in .streamlit/secrets.toml")

if __name__ == "__main__":
    main()