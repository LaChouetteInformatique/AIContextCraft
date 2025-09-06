"""API module for Lorem Ipsum service"""

from flask import Flask, jsonify
from main import LoremIpsumGenerator

app = Flask(__name__)
generator = LoremIpsumGenerator()

@app.route('/api/word')
def get_word():
    """Get a random word"""
    return jsonify({"word": generator.generate_word()})

@app.route('/api/sentence')
def get_sentence():
    """Get a random sentence"""
    return jsonify({"sentence": generator.generate_sentence()})

@app.route('/api/paragraph')
def get_paragraph():
    """Get a random paragraph"""
    return jsonify({"paragraph": generator.generate_paragraph()})
