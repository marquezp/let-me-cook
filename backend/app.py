from flask import Flask, jsonify
from flask_cors import CORS
from scrapy.crawler import CrawlerProcess
from scraper.spiders.quotes_spider import QuotesSpider
import os
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route('/scrape')
def scrape():
    output_file = "output.json"
    # Clean up previous output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)
        
    process = CrawlerProcess(settings={
        'FEEDS': {
            output_file: {'format': 'json'},
        },
        'LOG_ENABLED': False,
    })
    
    process.crawl(QuotesSpider)
    process.start()
    
    # Read the output file
    with open(output_file) as f:
        data = json.load(f)
    return jsonify(data)