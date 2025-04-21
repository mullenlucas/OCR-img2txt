from PIL import Image
import pytesseract

# Open an image file
image = Image.open("images/INSTRUCCIONES_CANDADO.jpeg")

# Extract text with bounding boxes
data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

# Loop through each text block
for i, word in enumerate(data["text"]):
    if word.strip():  # If the word isn't empty
        x, y, w, h = (
            data["left"][i],
            data["top"][i],
            data["width"][i],
            data["height"][i],
        )
        print(f"Word: {word} at position ({x}, {y}) with width {w} and height {h}")
