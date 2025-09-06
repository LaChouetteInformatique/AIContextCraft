#!/bin/bash
# Setup script to create test project structure for AI Context Craft

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEST_PROJECT_DIR="$SCRIPT_DIR/test-project"

echo -e "${BLUE}Creating test project structure...${NC}"

# Remove existing test project if it exists
if [ -d "$TEST_PROJECT_DIR" ]; then
    rm -rf "$TEST_PROJECT_DIR"
fi

# Create directory structure
mkdir -p "$TEST_PROJECT_DIR"/{backend,frontend/src/components,frontend/src/utils,docs,config,tests}

# Backend files
cat > "$TEST_PROJECT_DIR/backend/main.py" << 'EOF'
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
EOF

cat > "$TEST_PROJECT_DIR/backend/api.py" << 'EOF'
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
EOF

# Frontend files
cat > "$TEST_PROJECT_DIR/frontend/src/App.jsx" << 'EOF'
import React, { useState, useEffect } from 'react';
import LoremDisplay from './components/LoremDisplay';
import { fetchLorem } from './utils/api';

function App() {
  const [loremText, setLoremText] = useState('');
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    loadLorem();
  }, []);
  
  const loadLorem = async () => {
    setLoading(true);
    try {
      const text = await fetchLorem();
      setLoremText(text);
    } catch (error) {
      console.error('Failed to load lorem:', error);
    }
    setLoading(false);
  };
  
  return (
    <div className="app">
      <h1>Lorem Ipsum Generator</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <LoremDisplay text={loremText} />
      )}
      <button onClick={loadLorem}>Generate New</button>
    </div>
  );
}

export default App;
EOF

cat > "$TEST_PROJECT_DIR/frontend/src/components/LoremDisplay.jsx" << 'EOF'
import React from 'react';

const LoremDisplay = ({ text }) => {
  return (
    <div className="lorem-display">
      <p>{text || 'Click generate to create Lorem Ipsum text'}</p>
    </div>
  );
};

export default LoremDisplay;
EOF

cat > "$TEST_PROJECT_DIR/frontend/src/utils/api.js" << 'EOF'
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export async function fetchLorem(type = 'paragraph') {
  const response = await fetch(`${API_BASE}/api/${type}`);
  if (!response.ok) {
    throw new Error('Failed to fetch lorem text');
  }
  const data = await response.json();
  return data[type];
}
EOF

# Documentation files
cat > "$TEST_PROJECT_DIR/README.md" << 'EOF'
# Lorem Ipsum Generator

A simple Lorem Ipsum text generator with Python backend and React frontend.

## Features
- Generate random words
- Generate sentences
- Generate paragraphs

## Installation
```bash
pip install -r requirements.txt
npm install
```

## Usage
```bash
python backend/main.py
npm start
```
EOF

cat > "$TEST_PROJECT_DIR/docs/API.md" << 'EOF'
# API Documentation

## Endpoints

### GET /api/word
Returns a random Lorem Ipsum word.

### GET /api/sentence
Returns a random Lorem Ipsum sentence.

### GET /api/paragraph
Returns a random Lorem Ipsum paragraph.
EOF

# Configuration files
cat > "$TEST_PROJECT_DIR/config.yaml" << 'EOF'
app:
  name: Lorem Ipsum Generator
  version: 1.0.0
  
backend:
  host: localhost
  port: 5000
  
frontend:
  host: localhost
  port: 3000
EOF

cat > "$TEST_PROJECT_DIR/package.json" << 'EOF'
{
  "name": "lorem-ipsum-frontend",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
EOF

cat > "$TEST_PROJECT_DIR/requirements.txt" << 'EOF'
flask==2.3.0
pytest==7.4.0
EOF

# Test files
cat > "$TEST_PROJECT_DIR/tests/test_main.py" << 'EOF'
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
EOF

# Create some files to exclude
mkdir -p "$TEST_PROJECT_DIR"/{node_modules,venv/lib,.git,__pycache__,build,dist}
touch "$TEST_PROJECT_DIR/node_modules/package.json"
touch "$TEST_PROJECT_DIR/venv/lib/python.py"
touch "$TEST_PROJECT_DIR/.env"
echo "SECRET_KEY=do-not-include-this" > "$TEST_PROJECT_DIR/.env"
touch "$TEST_PROJECT_DIR/debug.log"
touch "$TEST_PROJECT_DIR/__pycache__/cache.pyc"

# Create .gitignore
cat > "$TEST_PROJECT_DIR/.gitignore" << 'EOF'
node_modules/
venv/
.venv/
__pycache__/
*.pyc
*.log
.env
.env.*
build/
dist/
EOF

echo -e "${GREEN}✅ Test project created successfully at: $TEST_PROJECT_DIR${NC}"
echo "Structure:"
tree -L 3 "$TEST_PROJECT_DIR" 2>/dev/null || {
    echo "backend/"
    echo "  ├── main.py"
    echo "  └── api.py"
    echo "frontend/"
    echo "  └── src/"
    echo "      ├── App.jsx"
    echo "      ├── components/"
    echo "      └── utils/"
    echo "docs/"
    echo "  ├── README.md"
    echo "  └── API.md"
    echo "tests/"
    echo "  └── test_main.py"
    echo "config.yaml"
    echo "package.json"
    echo "requirements.txt"
}