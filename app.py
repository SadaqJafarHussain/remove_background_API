from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image, ImageOps
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
    image = Image.open(io.BytesIO(output_image))

    # Ensure the image has an alpha channel (transparency)
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    # Create a white background image
    white_background = Image.new("RGBA", image.size, (255, 255, 255, 255))

    # Composite: Place the original image on top of the white background
    final_image = Image.alpha_composite(white_background, image)

    # Convert to RGB (removes alpha transparency)
    final_image = final_image.convert("RGB")

    # Save the final image to BytesIO
    output_io = io.BytesIO()
    final_image.save(output_io, format="PNG")
    output_io.seek(0)

    return send_file(output_io, mimetype='image/png')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Railway's port or default to 5000
    app.run(host="0.0.0.0", port=port)
