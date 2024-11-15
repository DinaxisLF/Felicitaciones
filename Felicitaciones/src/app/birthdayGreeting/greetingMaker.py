from fpdf import FPDF
from datetime import date, datetime
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage
import tempfile
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



def init_firebase():
    #load_dotenv()
    cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
    firebase_admin.initialize_app(cred, {"storageBucket": "tpe-project-31e9a.appspot.com"})

def upload_to_firebase(pdf_output_path, firebase_filename):
    bucket = storage.bucket()
    
    # Upload the file
    blob = bucket.blob(firebase_filename)
    blob.upload_from_filename(pdf_output_path)
    
    blob.make_public()
    # Get the URL of the uploaded file
    file_url = blob.public_url
    return file_url

def greeting_maker(docente,subject, body):
    name, lastname, email, id_docente = docente
    
    load_dotenv()
    current_date = datetime.now().strftime("%d %B %Y")

    # Create PDF in memory
    pdf = FPDF(orientation='L')
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Borders
    pdf.set_line_width(2)
    pdf.set_draw_color(212, 175, 55)
    pdf.rect(x=10, y=10, w=277, h=190, style='D')

    # Top Left Image
    left_image_path = os.path.join(os.getcwd(), 'src', 'app', 'static', 'images', 'UDG_Logo.png')
    pdf.image(left_image_path, x=30, y=20, w=40)

    # Title in the top middle
    pdf.set_xy(10, 40)
    pdf.set_font("Courier", size=20, style='B')
    pdf.cell(277, 10, txt="Felicitaciones", ln=True, align="C")

    # Top Right Image
    right_image_path = os.path.join(os.getcwd(), 'src', 'app', 'static', 'images', 'CUT_Logo.png')
    pdf.image(right_image_path, x=217, y=35, w=60)

    # Greeting Content
    pdf.set_xy(20, 85)
    pdf.set_font("Courier", size=11, style='BI')
    pdf.cell(0, 10, f"Estimado/a Profesor@, {name} {lastname}.", ln=True, align="L")

    pdf.set_xy(20, 95)
    pdf.multi_cell(0, 10, "En nombre de la Universidad de Guadalajara, es un honor\n"
                          "reconocer su valiosa contribucion al desarrollo académico\ny su compromiso con la formación de nuestros estudiantes.\n"
                          "Con profundo aprecio,\nRector del Centro Universitario De Tonala", align="L")

    # Sign
    sign_path = os.path.join(os.getcwd(), 'src', 'app', 'static', 'images', 'Firma.png')
    pdf.image(sign_path, x=120, y=143, w=60, h=40)

    # Date
    pdf.set_xy(110, 179)
    pdf.cell(80, 10, txt=current_date, ln=True, align="C")

    # Bottom right image
    btm_right_path = os.path.join(os.getcwd(), 'src', 'app', 'static', 'images', 'Leon.png')
    pdf.image(btm_right_path, x=215, y=100, w=70)

    # Create a temporary file to store the PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        pdf.output(temp_pdf.name)  # Save the PDF to the temporary file
        temp_pdf.seek(0)  # Go to the start of the file for reading

        # Initialize Firebase if not already done
        init_firebase()

        # Upload PDF to Firebase Storage
        firebase_filename = f"felicitaciones/Felicitaciones_{name}_{lastname}_{date.today()}.pdf"
        file_url = upload_to_firebase(temp_pdf.name, firebase_filename)

        print(f"PDF uploaded to Firebase: {file_url}")

        email = EmailSender()
        email.send_email(docente[2], subject, body, temp_pdf)

    return file_url  # Return the URL of the uploaded file