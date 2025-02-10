from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    uploaded_file = request.files['image']
    if uploaded_file.filename == '':
        return jsonify({"error": "Invalid image file"}), 400

    input_image = uploaded_file.read()
    output_image = remove(input_image)

    # Convert bytes to PIL image
    image = Image.open(io.BytesIO(output_image)).convert("RGBA")

    # Save the final image to BytesIO
    output_io = io.BytesIO()
    image.save(output_io, format="PNG")
    output_io.seek(0)

    return send_file(output_io, mimetype='image/png')

# No need for app.run() when using Gunicorn
