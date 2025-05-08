from flask import Flask, request, jsonify
from flask_cors import CORS
from pix2tex.cli import LatexOCR
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image part in the request"}), 400

        file = request.files['image']
        image = Image.open(file.stream).convert("RGB")

        # تحديد حجم الصورة
        max_size = (512, 512)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        model = LatexOCR()
        result = model(image)

        return jsonify({"latex": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

