import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from gtts import gTTS

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)

        if not image_list:
            print(f"No images found on page {page_num + 1}.")
            continue

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Convert image to text using pytesseract
            image = Image.open(io.BytesIO(image_bytes))
            text_from_image = pytesseract.image_to_string(image, lang="spa")  # Use "spa" for Spanish
            text += text_from_image + "\n"

            # Debug print
            print(f"Extracted text from page {page_num + 1}, image {img_index + 1}:")
            print(text_from_image)

    if not text.strip():
        print("Warning: No text was extracted from the PDF.")
    return text.strip()

def text_to_speech(text, audio_output_path):
    if not text:
        print("Error: No text to convert to speech.")
        return

    tts = gTTS(text=text, lang='es')  # Use 'es' for Spanish
    tts.save(audio_output_path)
    print(f"Audio saved to {audio_output_path}")

def pdf_to_audio_pipeline(pdf_path, audio_output_path):
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    print("Text extraction complete.")

    if text:
        print("Converting text to speech...")
        text_to_speech(text, audio_output_path)
        print("Pipeline complete.")
    else:
        print("No text found to convert to audio.")

# Example usage
pdf_path = "input.pdf"            # Path to the input PDF file
audio_output_path = "output.mp3"  # Path to save the audio file
pdf_to_audio_pipeline(pdf_path, audio_output_path)
