#!/usr/bin/env python3
"""Main application module for Lorem Ipsum Generator"""

import random
from typing import List, Optional

class LoremIpsumGenerator:
    """Generates Lorem Ipsum text"""
    
    def __init__(self):
        self.words = [
            "lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
            "adipiscing", "elit", "sed", "do", "eiusmod", "tempor"
        ]
    
    def generate_word(self) -> str:
        """Generate a random word"""
        return random.choice(self.words)
    
    def generate_sentence(self, word_count: int = 10) -> str:
        """Generate a sentence with specified number of words"""
        words = [self.generate_word() for _ in range(word_count)]
        words[0] = words[0].capitalize()
        return " ".join(words) + "."
    
    def generate_paragraph(self, sentence_count: int = 5) -> str:
        """Generate a paragraph with specified number of sentences"""
        sentences = [self.generate_sentence() for _ in range(sentence_count)]
        return " ".join(sentences)

def main():
    """Main entry point"""
    generator = LoremIpsumGenerator()
    print(generator.generate_paragraph())

if __name__ == "__main__":
    main()
