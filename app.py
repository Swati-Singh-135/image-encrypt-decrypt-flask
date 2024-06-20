from flask import Flask, request, render_template, send_file
import os
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files or 'number' not in request.form:
        return 'No file or number provided!', 400
    
    image = request.files['image']
    number = int(request.form['number'])
    
    if image.filename == '':
        return 'No selected file', 400

    # Read the image bytes
    image_bytes = image.read()
    encrypted_bytes = bytearray()

    # Encrypt the image bytes using XOR with the given number
    for byte in image_bytes:
        encrypted_bytes.append(byte ^ number)

    # Save the encrypted image in memory
    encrypted_image = BytesIO(encrypted_bytes)
    encrypted_image.seek(0)

    return send_file(encrypted_image, mimetype=image.mimetype, as_attachment=True, download_name=f'encrypted_{image.filename}')

if __name__ == '__main__':
    app.run(debug=True)
