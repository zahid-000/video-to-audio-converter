from flask import Flask, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import your_conversion_module  # Import your existing conversion code

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)
    
    # Generate output path
    output_filename = os.path.splitext(filename)[0] + '.mp3'
    output_path = os.path.join(RESULT_FOLDER, output_filename)
    
    # Convert video to MP3
    your_conversion_module.convert_video_to_mp3(input_path, output_path)
    
    # Return result
    return jsonify({
        'success': True,
        'download_url': f'/download/{output_filename}'
    })

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(RESULT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)