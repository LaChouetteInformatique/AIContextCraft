#!/usr/bin/env python3
"""
Token estimation utilities for AI Context Craft - Docker version
Tiktoken is pre-installed in the Docker image
"""

from typing import Optional, Dict, Tuple
import logging

class TokenEstimator:
    """Estimates token count for different LLM models"""
    
    def __init__(self):
        self.tiktoken_available = self._check_tiktoken()
        self.encoder = None
        self.model_limits = {
            'gpt-4': 8192,
            'gpt-4-32k': 32768,
            'gpt-4-turbo': 128000,
            'gpt-3.5-turbo': 4096,
            'gpt-3.5-turbo-16k': 16384,
            'claude-3-opus': 200000,
            'claude-3-sonnet': 200000,
            'claude-3-haiku': 200000,
            'gemini-pro': 32760,
            'gemini-1.5-pro': 1048576,  # 1M context
        }
        
        if self.tiktoken_available:
            self._initialize_tiktoken()
    
    def _check_tiktoken(self) -> bool:
        """Checks if tiktoken is available"""
        try:
            import tiktoken
            return True
        except ImportError:
            return False
    
    def _initialize_tiktoken(self):
        """Initializes tiktoken encoder"""
        try:
            import tiktoken
            # Use cl100k_base which is used by GPT-4 and GPT-3.5-turbo
            self.encoder = tiktoken.get_encoding("cl100k_base")
        except Exception as e:
            logging.warning(f"Failed to initialize tiktoken: {e}")
            self.tiktoken_available = False
    
    def estimate_tokens(self, text: str, method: str = "auto") -> Dict[str, any]:
        """
        Estimates the number of tokens in the text
        
        Args:
            text: Text to estimate
            method: Estimation method ('tiktoken', 'words', 'chars', 'auto')
            
        Returns:
            Dictionary with token count and metadata
        """
        result = {
            'method': method,
            'tokens': 0,
            'confidence': 'low',
            'details': {}
        }
        
        if method == "auto":
            if self.tiktoken_available:
                method = "tiktoken"
            else:
                method = "hybrid"
        
        if method == "tiktoken" and self.tiktoken_available:
            result['tokens'] = len(self.encoder.encode(text))
            result['confidence'] = 'high'
            result['method'] = 'tiktoken'
            result['details']['encoding'] = 'cl100k_base'
            
        elif method == "words":
            # Rough estimation: 1 token ≈ 0.75 words (GPT models)
            word_count = len(text.split())
            result['tokens'] = int(word_count / 0.75)
            result['confidence'] = 'medium'
            result['details']['word_count'] = word_count
            
        elif method == "chars":
            # Very rough: 1 token ≈ 4 characters
            result['tokens'] = len(text) // 4
            result['confidence'] = 'low'
            result['details']['char_count'] = len(text)
            
        elif method == "hybrid":
            # More sophisticated estimation without tiktoken
            word_count = len(text.split())
            char_count = len(text)
            
            # Different weights for different content types
            has_code = any(marker in text for marker in ['def ', 'function', 'import', 'class '])
            
            if has_code:
                # Code tends to have more tokens per character
                tokens_from_chars = char_count / 3.5
                tokens_from_words = word_count / 0.65
            else:
                # Natural language
                tokens_from_chars = char_count / 4.5
                tokens_from_words = word_count / 0.75
            
            # Weighted average
            result['tokens'] = int((tokens_from_chars + tokens_from_words) / 2)
            result['confidence'] = 'medium'
            result['details'] = {
                'word_count': word_count,
                'char_count': char_count,
                'detected_code': has_code
            }
        
        return result
    
    def estimate_file_tokens(self, file_path: str) -> Dict[str, any]:
        """Estimates tokens for a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.estimate_tokens(content)
        except Exception as e:
            return {
                'method': 'error',
                'tokens': 0,
                'confidence': 'none',
                'error': str(e)
            }
    
    def fits_in_context(self, token_count: int, model: str) -> Tuple[bool, float]:
        """
        Checks if token count fits in model context
        
        Returns:
            Tuple of (fits: bool, usage_percentage: float)
        """
        if model not in self.model_limits:
            return (None, 0.0)
        
        limit = self.model_limits[model]
        fits = token_count <= limit
        usage = (token_count / limit) * 100
        
        return (fits, usage)
    
    def get_recommendation(self, token_count: int) -> str:
        """Returns a recommendation based on token count"""
        recommendations = []
        
        for model, limit in sorted(self.model_limits.items(), key=lambda x: x[1]):
            if token_count <= limit:
                usage = (token_count / limit) * 100
                if usage <= 80:  # Good fit
                    recommendations.append(f"✅ {model} ({usage:.1f}% of context)")
                elif usage <= 95:  # Tight fit
                    recommendations.append(f"⚠️  {model} ({usage:.1f}% of context)")
                
                if len(recommendations) >= 3:  # Show top 3 recommendations
                    break
        
        if not recommendations:
            return "❌ Token count exceeds all standard model contexts. Consider splitting the content."
        
        return "\n".join(["📊 Model recommendations:"] + recommendations)
    
    def format_summary(self, estimation: Dict[str, any], include_models: bool = True) -> str:
        """Formats a nice summary of the estimation"""
        lines = []
        
        tokens = estimation['tokens']
        confidence = estimation['confidence']
        method = estimation['method']
        
        # Token count with confidence indicator
        confidence_emoji = {'high': '🎯', 'medium': '📊', 'low': '⚠️'}.get(confidence, '❓')
        lines.append(f"{confidence_emoji} Estimated tokens: {tokens:,}")
        
        # Method used
        method_desc = {
            'tiktoken': 'Precise OpenAI tokenizer',
            'hybrid': 'Advanced heuristic',
            'words': 'Word-based estimation',
            'chars': 'Character-based estimation'
        }.get(method, method)
        lines.append(f"   Method: {method_desc}")
        
        # Additional details
        if 'details' in estimation:
            if 'word_count' in estimation['details']:
                lines.append(f"   Words: {estimation['details']['word_count']:,}")
            if 'detected_code' in estimation['details']:
                if estimation['details']['detected_code']:
                    lines.append(f"   Content type: Code detected")
        
        # Model recommendations
        if include_models:
            lines.append("")
            lines.append(self.get_recommendation(tokens))
        
        return "\n".join(lines)