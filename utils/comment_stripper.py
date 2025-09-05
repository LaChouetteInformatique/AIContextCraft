#!/usr/bin/env python3
"""
Module to remove comments from source code using tree-sitter
for robust syntax analysis.
"""
from typing import Optional, Dict
from tree_sitter import Parser, Language
from tree_sitter_languages import get_language, get_parser

class CommentStripper:
    """Removes comments from code files using tree-sitter."""

    def __init__(self):
        self._parsers: Dict[str, Parser] = {}
        self._languages: Dict[str, Language] = {}
        self._language_map: Dict[str, str] = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.sh': 'bash',
            '.bash': 'bash',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.h': 'c',
            '.hpp': 'cpp',
            '.css': 'css',
            '.html': 'html',
        }

    def _get_parser(self, file_type: str) -> Optional[Parser]:
        """Loads and caches the parser for a given file type."""
        if file_type not in self._language_map:
            return None
        
        lang_name = self._language_map[file_type]
        
        if lang_name not in self._parsers:
            try:
                language = get_language(lang_name)
                parser = get_parser(lang_name)
                self._languages[lang_name] = language
                self._parsers[lang_name] = parser
            except Exception as e:
                # The grammar may not be installed, which is a recoverable issue.
                print(f"Warning: Could not load grammar for '{lang_name}': {e}")
                return None
        
        return self._parsers[lang_name]

    def strip_comments(self, content: str, file_path: str) -> str:
        """
        Removes comments from a content string based on its file type.
        
        Args:
            content: The source file content.
            file_path: The file path to determine the language.
            
        Returns:
            The content without comments, or the original content if the language is not supported.
        """
        file_ext = '.' + file_path.split('.')[-1]
        parser = self._get_parser(file_ext)

        if not parser:
            return content

        try:
            tree = parser.parse(bytes(content, "utf8"))
            new_content_parts = []
            last_index = 0

            lang_name = self._language_map[file_ext]
            language = self._languages[lang_name]
            
            # The names of comment nodes can vary between grammars.
            comment_query_str = "((comment) @comment)"
            if lang_name in ['python', 'ruby']:
                 # This logic can be refined, but for simplicity, we use a broad query.
                 comment_query_str = "((comment) @comment) ((string) @string)"

            query = language.query(comment_query_str)
            captures = query.captures(tree.root_node)

            for node, _ in captures:
                if 'comment' in node.type:
                    new_content_parts.append(content[last_index:node.start_byte])
                    # Replace the comment with newlines to preserve line numbers,
                    # which can be important for error reporting and analysis.
                    comment_text = content[node.start_byte:node.end_byte]
                    num_lines = comment_text.count('\n')
                    new_content_parts.append('\n' * num_lines)
                    last_index = node.end_byte
            
            new_content_parts.append(content[last_index:])

            return "".join(new_content_parts)

        except Exception:
            # In case of a parsing error (e.g., invalid syntax in the source file),
            # fall back to returning the original content to avoid crashing the process.
            return content