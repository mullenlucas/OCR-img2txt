import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Define a font mapping
FONT_MAP = {
    "timesnewromanpsmt": "Times-Roman",
    "timesnewromanps-boldmt": "Times-Bold",
    "timesnewromanps-italicmt": "Times-Italic",
    "arialmt": "Helvetica",
    "arial-boldmt": "Helvetica-Bold",
    "arial-italicmt": "Helvetica-Oblique",
    # Add other font mappings as needed
}

def map_font_name(font_name, is_bold, is_italic):
    # Convert the font name to lower case to ensure case insensitivity
    font_name = font_name.lower()

    # Adjust based on bold and italic flags
    if is_bold and is_italic:
        return FONT_MAP.get(font_name + "-bolditalic", "Helvetica-BoldOblique")
    elif is_bold:
        return FONT_MAP.get(font_name + "-boldmt", "Helvetica-Bold")
    elif is_italic:
        return FONT_MAP.get(font_name + "-italicmt", "Helvetica-Oblique")
    else:
        return FONT_MAP.get(font_name, "Helvetica")

def create_pdf_with_text_and_images(pdf_path, output_pdf_path, header_y_limit=100, footer_y_limit=750):
    doc = fitz.open(pdf_path)
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    bbox = span["bbox"]
                    y0, y1 = bbox[1], bbox[3]
                    text = span["text"]
                    font_size = span["size"]
                    font_name = span["font"]
                    is_bold = "Bold" in font_name or "bold" in font_name
                    is_italic = "Italic" in font_name or "italic" in font_name

                    # Skip headers and footers based on y-coordinate
                    if y0 > header_y_limit and y1 < footer_y_limit and text.strip():
                        # Map the font name to a PostScript font name
                        font_ps_name = map_font_name(font_name, is_bold, is_italic)
                        c.setFont(font_ps_name, font_size)
                        c.drawString(bbox[0], height - y0, text)

        # Process images
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))

            # Save image as a temp file
            image_filename = f"temp_image_{page_num + 1}_{img_index + 1}.png"
            image.save(image_filename)

            # Draw the image in the PDF
            c.drawImage(image_filename, bbox[0], height - bbox[3], width=(bbox[2]-bbox[0]), height=(bbox[3]-bbox[1]))

        c.showPage()  # Start a new page

    c.save()
    print(f"New PDF with modified content saved as {output_pdf_path}")

# Example usage
pdf_path = "input.pdf"          # Path to the original PDF file
output_pdf_path = "output.pdf"  # Path to save the new PDF file
create_pdf_with_text_and_images(pdf_path, output_pdf_path)
