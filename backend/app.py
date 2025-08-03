from flask import Flask, jsonify
from flask_cors import CORS
import os
import json
import subprocess

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route('/scrape')
def scrape():
    output_file = "output.json"
    # Clean up previous output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    result = subprocess.run(['scrapy', 'crawl', 'recipespider', '-o', 'output.json'], capture_output=True, text=True)

    if result.returncode == 0:
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify({"status": "success", "data": data})
    else:
        return jsonify({"status": "error", "details": result.stderr}), 500