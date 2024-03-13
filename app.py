from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import spacy

app = Flask(__name__)

# Load the English language model for spaCy
nlp = spacy.load('en_core_web_sm')

# Function to extract invoice attributes using spaCy's NER
def extract_invoice_attributes(text):
    doc = nlp(text)

    invoice_number = None
    invoice_date = None
    invoice_amount = None

    for ent in doc.ents:
        if ent.label_ == 'DATE':
            invoice_date = ent.text
        elif ent.label_ == 'CARDINAL':  # 'CARDINAL' label is used for numerical entities like invoice number and amount
            if not invoice_number:
                invoice_number = ent.text
            elif not invoice_amount:
                invoice_amount = ent.text

    return invoice_number, invoice_date, invoice_amount

# REST API endpoint for extracting invoice attributes from an image
@app.route('/extract_invoice_attributes', methods=['POST'])
def extract_invoice_attributes_from_image():
    # Check if file is provided in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    # Read image file from the request
    file = request.files['file']
    img = Image.open(file)

    # Perform OCR to extract text from the image
    text = pytesseract.image_to_string(img)
    print(text)
    # Extract invoice attributes from the extracted text
    invoice_number, invoice_date, invoice_amount = extract_invoice_attributes(text)

    # Return extracted attributes in JSON format
    return jsonify({
        'invoice_number': invoice_number,
        'invoice_date': invoice_date,
        'invoice_amount': invoice_amount
    })

if __name__ == '__main__':
    app.run(debug=True)
