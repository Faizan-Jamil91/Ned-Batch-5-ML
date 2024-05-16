import smtplib
from email.mime.text import MIMEText

def send_registration_email(email, username):
    gmail_username = "faizanjamil51@gmail.com"
    gmail_password = ""  # Use app password or enable less secure app access
    smtp_server = "accounts.google.com"
    smtp_port = 587  # Gmail SMTP port
    sender_email = gmail_username

    receiver_email = email
    subject = "Registration Confirmation"
    message = f"Subject: {subject}\n\nDear {username},\n\nYou have successfully registered your account. Thank you!\n\nBest regards,\nThe Team"

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(gmail_username, gmail_password)
        server.sendmail(sender_email, receiver_email, message)
