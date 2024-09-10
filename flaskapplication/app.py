from flask import Flask, render_template, request, jsonify
from lang_detection import test_language
from waitress import serve

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect_language', methods=['POST'])
def detect_language():
    paragraph = request.form['paragraph']
    language = test_language(paragraph)
    print(language)
    return render_template('result.html', language=language)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)