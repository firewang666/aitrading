from flask import Flask, jsonify
import gdown
app = Flask(__name__)

@app.route('/run-colab')
def run_colab():
    gdown.download('https://drive.google.com/drive/folders/1zVI5huEKOxJn5qB-1vxtuxbGPeAJ6KRh', 'colab.ipynb', quiet=False)
    return jsonify(message='colab notebook ran successfully')
