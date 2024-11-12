from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

# Replace 'your_directory' with the directory where your ZIP is extracted
your_directory = os.path.join(os.getcwd(), "Project")

@app.route('/')
def index():
    # Serve index.html from the extracted directory
    return send_from_directory(your_directory, 'index.html')

@app.route('/get')
def text():
    return 'I got it !'

@app.route('/<path:filename>')
def serve_file(filename):
    # Serve other files (like JS, CSS) from the extracted directory
    return send_from_directory(your_directory, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)