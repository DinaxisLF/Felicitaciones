from fpdf import FPDF
from datetime import date
import os

def greeting_maker(docente):
    name, lastname, email, id_docente = docente


    #Create PDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Set the outer border color (e.g., blue) and fill it
    pdf.set_fill_color(212, 175, 55)  # Light blue fill for the border
    pdf.rect(0, 0, 297, 210, 'F')  # Fill the outer rectangle


    # Set the inner rectangle
    pdf.set_fill_color(255, 255, 255)  # White fill for the inner rectangle
    pdf.rect(10, 10, 277, 190, 'F')  # Fill the inner rectangle (10mm margin on all sides)
    

    #Top Left Image
    left_image_path = os.path.join(os.getcwd(), 'src', 'app','static', 'images', 'UDG_Logo.png')
    pdf.image(left_image_path, x=15, y=25, w=50, h=50)  # Adjust the width as needed

    # Title in the top middle
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Feliz Cumpleaños!", ln=True, align="C")  # Centered title

    # Top Right Image
    right_image_path = os.path.join(os.getcwd(), 'src', 'app', 'static', 'images', 'CUT_Logo.png')
    pdf.image(right_image_path, x=247, y=10, w=40)  # Adjust the width as needed

    # Content starts after the title
    pdf.set_font("Arial", "", 12)
    pdf.ln(20)  # Add space after the title and images
    pdf.cell(0, 10, f"Estimado/a {name} {lastname},", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, "Te deseamos un muy feliz cumpleaños. Que tengas un gran día lleno de alegría y éxito.\n\n"
                        "Con nuestros mejores deseos,\nEl equipo.")
    
    # Save PDF to a specified path
    pdf_filename = f"Felicitacion_docente {id_docente}_{date.today()}.pdf"
    pdf_output_path = "C:\\Users\\cesar\\Desktop\\UdeG\\Agil\\PDFs\\" + pdf_filename
    pdf.output(pdf_output_path)
    
    print(f"PDF generated for {name} {lastname} at {pdf_output_path}")