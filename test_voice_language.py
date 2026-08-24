import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from voice_alert import speak

print("Testing voice alerts in different languages...")

# Test English
print("1. Testing English voice alert...")
speak("It's time to take Paracetamol.", "en")

print("\n2. Testing Bangla voice alert...")
speak("প্যারাসিটামল খাওয়ার সময় হয়েছে।", "bn")

print("\n3. Testing medicine reminder in English...")
speak("It's time to take your medicine.", "en")

print("\n4. Testing medicine reminder in Bangla...")
speak("আপনার ওষুধ খাওয়ার সময় হয়েছে।", "bn")

print("\nVoice language test completed!")