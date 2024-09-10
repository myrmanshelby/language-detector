from flask import Flask, render_template, request, jsonify
from lang_detection import test_language
import os

print(os.getcwd())

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
    app.run()