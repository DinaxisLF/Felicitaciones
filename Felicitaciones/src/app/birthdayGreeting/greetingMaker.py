from fpdf import FPDF
from datetime import date, datetime
import os
from dotenv import load_dotenv
import webbrowser




def greeting_maker(docente):
    
    name, lastname, email, id_docente = docente
    
    load_dotenv()
    current_date = datetime.now().strftime("%d %B %Y")

    # Create PDF
    pdf = FPDF()
    pdf = FPDF(orientation='L')
    # Add a page
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size=12)

    #Borders
    pdf.set_line_width(2)
    pdf.set_draw_color(212, 175, 55)
    # Draw a border
    pdf.rect(x=10, y=10, w=277, h=190, style='D')  # Drawing a border around the page
    

    #Top Left Image
    left_image_path = os.path.join(os.getcwd(), 'src', 'app','static', 'images', 'UDG_Logo.png')
    pdf.image(left_image_path, x=30, y=20, w=40)  # Adjust the width as needed

    # Title in the top middle
    pdf.set_xy(10, 40)
    pdf.set_font("Courier", size=20, style='B')
    pdf.cell(277, 10, txt="Felicitaciones", ln=True, align="C")

    # Top Right Image
    right_image_path = os.path.join(os.getcwd(), 'src', 'app', 'static', 'images', 'CUT_Logo.png')
    pdf.image(right_image_path, x=217, y=35, w=60)  # Adjust the width as needed

    #Greeting Content
    pdf.set_xy(20,85)
    pdf.set_font("Courier", size=11, style='BI')
    pdf.cell(0, 10, f"Estimado/a Profesor@, {name} {lastname}.", ln=True, align="L")

    pdf.set_xy(20,95)
    pdf.multi_cell(0, 10, "En nombre de la Universidad de Guadalajara, es un honor\n"
                        "reconocer su valiosa contribucion al desarrollo académico\ny su compromiso con la formación de nuestros estudiantes.\n"
                        "Con profundo aprecio,\nRector del Centro Universitario De Tonala",align="L")
    

    #Sign
    sign_path = os.path.join(os.getcwd(), 'src', 'app', 'static', 'images', 'Firma.png')
    pdf.image(sign_path, x=120, y=143, w=60, h=40)

    #Date
    pdf.set_xy(110, 179)  # Adjust the y value to position the date text below the bottom image
    pdf.cell(80, 10, txt=current_date, ln=True, align="C")

    #Bottom righ image
    btm_right_path = os.path.join(os.getcwd(), 'src', 'app', 'static', 'images', 'Leon.png')
    pdf.image(btm_right_path, x=215, y=100, w=70)

    # Save PDF to a specified path
    pdf_filename = f"Felicitacion_docente {id_docente}_{date.today()}.pdf"
    pdf_output_path = os.getenv('PDF_PATH_SAVE') + pdf_filename
    pdf.output(pdf_output_path)
    
    print(f"PDF generated for {name} {lastname} at {pdf_output_path}")

    #Open PDF
    webbrowser.open(pdf_output_path)