from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from enhanced_analyzer import EnhancedResumeAnalyzer
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Use PDF or DOCX'})
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(tempfile.gettempdir(), filename)
        file.save(temp_path)
        
        try:
            # Analyze resume
            analyzer = EnhancedResumeAnalyzer()
            analysis = analyzer.enhanced_analyze_resume(temp_path)
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass  # Ignore cleanup errors
            
            if 'error' in analysis:
                return jsonify({'error': analysis['error']})
            
            return jsonify({
                'success': True,
                'analysis': analysis,
                'report': analyzer.generate_enhanced_report(analysis)
            })
            
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)