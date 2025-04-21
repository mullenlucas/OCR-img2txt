from PIL import Image
import pytesseract
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust for Windows
)

# Step 1: Load image and extract text
image_path = "images/intrux.jpg"  # Replace with your image file path
image = Image.open(image_path)

# Extract the text from the image using pytesseract
extracted_text = pytesseract.image_to_string(image)

# Step 2: Create a PDF with ReportLab
pdf_filename = "formatted_output_instructions.pdf"
pdf = canvas.Canvas(pdf_filename, pagesize=letter)

# Set font sizes for different types of text
heading_font_size = 16
list_font_size = 12
regular_font_size = 10

# Starting coordinates for the text
x_offset = 100  # X position of the text on the page
y_offset = 750  # Start near the top of the page

# Split extracted text into lines
lines = extracted_text.splitlines()

# Step 3: Format and write the text into the PDF
for line in lines:
    # Clean up line (remove extra spaces)
    clean_line = line.strip()

    # Skip empty lines
    if not clean_line:
        y_offset -= 20
        continue

    # Heading Detection: Auto-center text if it seems like a heading (you can define your own logic)
    if clean_line.lower().startswith("instructions:"):
        pdf.setFont("Helvetica-Bold", heading_font_size)
        pdf.drawCentredString(300, y_offset, clean_line)
        y_offset -= 40  # More space after headings

    # List Detection: Auto-indent text if it starts with a number or bullet point
    elif clean_line[0].isdigit() or clean_line.startswith("-"):
        pdf.setFont("Helvetica", list_font_size)
        # Add indentation for list items
        pdf.drawString(x_offset + 20, y_offset, clean_line)
        y_offset -= 20  # Less space between list items

    # Regular Paragraphs: Left-align regular text
    else:
        pdf.setFont("Helvetica", regular_font_size)
        # Add left-aligned regular text
        pdf.drawString(x_offset, y_offset, clean_line)
        y_offset -= 20  # Standard space between paragraphs

    # Move to next page if y_offset is too low
    if y_offset < 50:
        pdf.showPage()
        y_offset = 750  # Reset y_offset for the new page

# Save the PDF
pdf.save()

print(f"PDF saved as {pdf_filename}")
