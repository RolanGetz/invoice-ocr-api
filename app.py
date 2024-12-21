from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)

# Получение токена из переменных окружения
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Invoice OCR API! Use the /process-invoice endpoint to process invoices.", 200

@app.route('/process-invoice', methods=['POST'])
def process_invoice():
    # Проверка токена
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization header is missing or invalid"}), 401

    token = auth_header.split("Bearer ")[1]
    if token != BEARER_TOKEN:
        return jsonify({"error": "Invalid token"}), 403

    # Работа с файлом накладной
    file = request.files.get('invoice')
    if not file:
        return jsonify({"error": "Invoice file is required"}), 400

    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return jsonify({"recognized_text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
