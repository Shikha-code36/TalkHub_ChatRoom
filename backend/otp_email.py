import random
import smtplib
from email.mime.text import MIMEText
from fastapi import HTTPException
from constant import *
from cachetools import TTLCache

# Function to generate OTP
def generate_otp(length: int = 6):
    return str(random.randint(10 ** (length - 1), (10 ** length) - 1))

# Function to send OTP via email
def send_otp(email, otp):
    import pdb;pdb.set_trace()
    # Set up email configuration
    sender_email = SENDEREMAIL

    # Compose the email message
    subject = "OTP Verification"
    body = f"Your OTP is: {otp}"
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = email

    try:
        with smtplib.SMTP_SSL(SOURCE, PORT) as server:
            # Connect to the SMTP server and send the email
            server.ehlo()
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(sender_email, email, message.as_string())
        
            # Close the SMTP server
            server.quit()

    except Exception as e:
        # Handle email sending errors
        raise HTTPException(status_code=500, detail="Failed to send OTP")

# Create a TTLCache for storing OTPs
otp_cache = TTLCache(maxsize=100, ttl=600)  # Maximum 100 OTPs with a TTL of 600 seconds (10 minutes)

def get_stored_otp(email):
    return otp_cache.get(email)

def store_otp(email, otp):
    otp_cache[email] = otp

# Function to verify OTP
def verify_otp(email, otp):
    stored_otp = get_stored_otp(email)
    if stored_otp and otp == stored_otp:
        return True
    else:
        return False
