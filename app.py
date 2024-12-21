from flask import Flask, request, jsonify
from PIL import Image
import pytesseract

app = Flask(__name__)

@app.route('/process-invoice', methods=['POST'])
def process_invoice():
    file = request.files['invoice']
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return jsonify({"recognized_text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
