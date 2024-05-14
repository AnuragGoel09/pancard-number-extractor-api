from flask import Flask, request, jsonify
import easyocr
import cv2
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

reader = easyocr.Reader(['en'])
@app.route('/upload',methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'error': 'No selected image'}), 400

    try:
        image=image_file.read()
        nparr = np.frombuffer(image, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        pan_number=get_pan_number(image)
        return jsonify({'text': pan_number}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_pan_number(image):
    extracted_text = reader.readtext(image)
    result= [entry[1] for entry in extracted_text]
    
    for i in result:
        if len(i)==0:
            result.remove(i)
    for item in result:
        if len(item)==10:
            check=True
            for i in item:
                if (i>='A' and i<='Z') or (i>='0' and i<='9'):
                    a=1
                else:
                    check=False
                    break
            if check:
                flag=check_pan(item)
                if flag:
                    return item
    return "Image is not proper"
def check_pan(name):
    if len(name)!=10:
        return False
    check=True
    for i in range(5):
        if name[i]>='A' and name[i]<='Z':
            check=True
        else:
            return False
    for i in range(5,9):
        if name[i]>='0' and name[i]<='9':
            check=True
        else:
            return False
    if name[-1]>='A' and name[-1]<='Z':
        check=True
    else:
        return False
    return True


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port='4000')