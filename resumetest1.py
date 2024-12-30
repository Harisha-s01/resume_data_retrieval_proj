import mysql.connector
from PyPDF2 import PdfReader
import re
import os

print("Starting the script...")

def extract_phone_and_email(text):
    print("Extracting phone numbers and emails...")
    phone_pattern = r"\b\d{10}\b"
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    phone_numbers = re.findall(phone_pattern, text)
    emails = re.findall(email_pattern, text)
    print(f"Found phone numbers: {phone_numbers}")
    print(f"Found emails: {emails}")
    return phone_numbers, emails

print("Checking file path...")

file_path = r"C:\Users\haris\OneDrive\Desktop\intern_proj\HarishaS_Resume_1.pdf"
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit()

print(f"File found: {file_path}")

try:
    print("Reading PDF...")
    reader = PdfReader(file_path)
    resume_content = ""
    for page in reader.pages:
        resume_content += page.extract_text()
    print("PDF content extracted successfully.")
except Exception as e:
    print(f"Error reading PDF: {e}")
    exit()

phone_numbers, emails = extract_phone_and_email(resume_content)

try:
    print("Connecting to database...")
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Harisha#8",
        database="haridb 1"
    )
    print("Database connected successfully.")
except mysql.connector.Error as err:
    print(f"Database connection error: {err}")
    exit()

cursor = db.cursor()

try:
    print("Inserting data into database...")
    for phone in phone_numbers:
        for email in emails:
            sql = "INSERT INTO resumetest (phonenumber, email) VALUES (%s, %s)"
            values = (phone, email)
            print(f"Executing SQL: {sql} with values {values}")
            cursor.execute(sql, values)
    db.commit()
    print(f"Inserted {cursor.rowcount} record(s).")
except mysql.connector.Error as err:
    print(f"SQL Error: {err}")
finally:
    cursor.close()
    db.close()
    print("Database connection closed.")

print("Script completed.")

