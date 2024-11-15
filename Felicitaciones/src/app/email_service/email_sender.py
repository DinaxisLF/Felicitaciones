import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from dotenv import load_dotenv
from email import encoders



class EmailSender:
    def __init__(self):
        load_dotenv()
        self.mail_user = os.getenv('MAIL_USER')
        self.mail_password = os.getenv('MAIL_PASS')
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
    
    #Send Emails
    def send_email(self, recipient_email, subject, body, pdf_buffer):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.mail_user
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

    

                # Attach the PDF file
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(pdf_buffer.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="Felicitaciones.pdf"')
            msg.attach(part)

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.mail_user, self.mail_password)
            server.send_message(msg)
            server.quit()

            print(f"Email sent to {recipient_email}")

        except Exception as e:
            print(f"Failed to send email: {e}")
