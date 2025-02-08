from flask import Flask, request, jsonify
from rembg import remove
import base64

app = Flask(__name__)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    uploaded_file = request.files['image']
    if uploaded_file.filename != '':
        input_image = uploaded_file.read()
        output_image = remove(input_image)
        
        # Convert to base64
        encoded_original = base64.b64encode(input_image).decode('utf-8')
        encoded_modified = base64.b64encode(output_image).decode('utf-8')

        return jsonify({
            "original_image": f'data:image/png;base64,{encoded_original}',
            "modified_image": f'data:image/png;base64,{encoded_modified}'
        })
    else:
        return jsonify({"error": "Invalid image file"}), 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
