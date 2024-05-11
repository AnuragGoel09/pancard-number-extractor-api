# app.py

from flask import Flask, request, jsonify 
from PIL import Image
import pytesseract
import io

app = Flask(__name__)

@app.route('/upload',methods=['GET'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected image'}), 400

    try:
        # Read image from the file upload
        image = Image.open(io.BytesIO(image_file.read()))

        # Perform OCR using pytesseract
        extracted_text = pytesseract.image_to_string(image)

        return jsonify({'text': extracted_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
