import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

# Set up Tesseract OCR (ensure Tesseract is installed and available in your PATH)
# If Tesseract is not in your PATH, specify the full path to the executable.
# Example: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    extracted_text = ""

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]  # Reference to the image
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]

            # Convert image bytes to a PIL image
            image = Image.open(io.BytesIO(image_bytes))

            # Perform OCR on the image
            text = pytesseract.image_to_string(image)
            extracted_text += (
                f"\nPage {page_number + 1}, Image {img_index + 1}:\n{text}\n"
            )

    pdf_document.close()
    return extracted_text


# Specify the path to your PDF
pdf_path = "images/sols.pdf"

# Extract text from the PDF
text = extract_text_from_pdf(pdf_path)

# Print or save the extracted text
print(text)
