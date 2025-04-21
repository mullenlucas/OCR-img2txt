from PIL import Image
import pytesseract

# Open an image file
image = Image.open("images/sols_Page1.png")

# Extract text from image
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)
