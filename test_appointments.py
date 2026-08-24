#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script to verify appointment alert mechanism"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# Connect to the database
conn = sqlite3.connect("medicine.db")

# Check if appointments table exists
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='appointments'")
if not cursor.fetchone():
    print("❌ Appointments table does not exist!")
    conn.close()
    exit(1)

print("✓ Appointments table exists")

# Check table structure
cursor.execute("PRAGMA table_info(appointments)")
columns = {row[1]: row[2] for row in cursor.fetchall()}
print(f"✓ Columns: {list(columns.keys())}")

required_cols = ['email_notified', 'voice_notified']
for col in required_cols:
    if col not in columns:
        print(f"❌ Missing column: {col}")
    else:
        print(f"✓ Column exists: {col}")

# List all appointments
print("\n--- All Appointments ---")
appts = pd.read_sql_query("SELECT * FROM appointments", conn)
print(f"Total appointments: {len(appts)}")
for _, row in appts.iterrows():
    print(f"  ID={row['id']}: {row['doctor_name']} on {row['date']} at {row['time']}")
    print(f"    email_notified={row.get('email_notified')}, voice_notified={row.get('voice_notified')}")

# Check for unnotified appointments in the next hour
print("\n--- Appointments in next 1 hour that need alerts ---")
now = datetime.now()
future = now + timedelta(hours=1)

query = """
    SELECT * FROM appointments 
    WHERE (email_notified=0 OR voice_notified=0)
    AND datetime(date || ' ' || time) BETWEEN datetime('now') AND datetime('now', '+1 hour')
"""
upcoming = pd.read_sql_query(query, conn)
print(f"Found {len(upcoming)} appointments needing alerts in next hour")
for _, row in upcoming.iterrows():
    ap_dt = datetime.strptime(f"{row['date']} {row['time']}", "%Y-%m-%d %H:%M")
    diff = (ap_dt - now).total_seconds()
    print(f"  {row['doctor_name']}: {diff:.0f} seconds away (email={row.get('email_notified')}, voice={row.get('voice_notified')})")

conn.close()
print("\n✓ Test complete")
