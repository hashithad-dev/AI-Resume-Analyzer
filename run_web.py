from app import app

if __name__ == '__main__':
    print("Starting Resume Analyzer Web Interface...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)