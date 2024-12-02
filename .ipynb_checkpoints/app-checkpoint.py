from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
import numpy as np
import easyocr

# Config
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
app = Flask(__name__)
CORS(app)
reader = easyocr.Reader(['en'], gpu=False)

def process_image(image, method):
    if method == 'original':
        return image  # Trả về ảnh gốc không xử lý
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if method == 'otsu':
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        return thresh
    elif method == 'distance_transform':
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
     
        dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
        return (dist * 255).astype("uint8")
    elif method == 'morphological_opening':
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
        dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        opening = cv2.morphologyEx(dist, cv2.MORPH_OPEN, kernel)
        return (opening * 255).astype("uint8")
    else:
        return gray



@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    method = request.form.get('method')

    if not file:
        return jsonify({'error': 'No file provided'}), 400

    # Load image
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Process image
    processed_image = process_image(img, method)
    _, buffer = cv2.imencode('.jpg', processed_image)
    processed_image_base64 = buffer.tobytes()

    # OCR
    result = reader.readtext(processed_image)
    text = "\n".join([res[1] for res in result])

    return jsonify({
        'processed_image': processed_image_base64.decode('latin1'),
        'ocr_text': text
    })

if __name__ == '__main__':
    app.run(debug=True)
