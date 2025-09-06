"""Tests for main module"""

import sys
sys.path.insert(0, '../backend')

from main import LoremIpsumGenerator

def test_generate_word():
    generator = LoremIpsumGenerator()
    word = generator.generate_word()
    assert isinstance(word, str)
    assert len(word) > 0

def test_generate_sentence():
    generator = LoremIpsumGenerator()
    sentence = generator.generate_sentence()
    assert sentence.endswith('.')
    assert sentence[0].isupper()

def test_generate_paragraph():
    generator = LoremIpsumGenerator()
    paragraph = generator.generate_paragraph()
    assert '.' in paragraph
    assert len(paragraph) > 50
