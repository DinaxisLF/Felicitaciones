import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from flask import jsonify, request
from app.email_service import email_sender_class


class EmailSender:
    def __init__(self):
        load_dotenv()
        self.mail_user = os.getenv('MAIL_USER')
        self.mail_password = os.getenv('MAIL_PASS')
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
    
    def send_email(self, recipient_email, subject, body):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.mail_user
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.mail_user, self.mail_password)
            server.send_message(msg)
            server.quit()

            print(f"Email sent to {recipient_email}")

        except Exception as e:
            print(f"Failed to send email: {e}")

@email_sender_class.route('/email_sender', methods=['POST'])
def send_email():
    try:
        # Get data from the request
        data = request.get_json()
        recipient_email = data.get('email')
        subject = data.get('subject')
        body = data.get('body')
        
        # Initialize EmailSender
        email_sender = EmailSender()
        
        # Send the email
        email_sender.send_email(recipient_email, subject, body)

        return jsonify({"message": "Email sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500