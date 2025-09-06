#!/usr/bin/env python3
"""
AI Context Craft - Main Module
Tool for preparing code context for LLMs
Docker version with Git integration and advanced tree generation
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from utils.app import AIContextCraft

def main():
    """Main entry point""" 
    parser = argparse.ArgumentParser(
        description="""AI Context Craft - Prepare your code for LLMs
        
Transform your codebase into AI-ready context with intelligent filtering,
Git integration, and advanced tree visualization.

Features:
  • Smart filtering with gitignore-style patterns
  • Git-aware file selection (tracked/untracked)
  • Multiple tree visualization modes
  • Comment stripping for token optimization
  • Direct clipboard copy (Linux/X11)
  • Accurate token estimation with tiktoken
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s                      # Process current directory
  %(prog)s . --git-only         # Only Git-tracked files
  %(prog)s . --with-tree        # Include project structure
  %(prog)s . --strip-comments   # Remove comments to save tokens
  %(prog)s . --to-clipboard     # Copy directly to clipboard

Configuration:
  Create concat-config.yaml in your project for custom filtering.
  See https://github.com/YOUR_USERNAME/ai-context-craft for docs.
        """
    )
    
    parser.add_argument(
        "source", 
        nargs='?',
        default=".",
        help="Source directory to process (default: current directory)"
    )
    
    parser.add_argument(
        "-o", "--output", 
        help="Output file path (default: build/project_files_TIMESTAMP.txt)"
    )
    
    # Git integration
    git_group = parser.add_argument_group('Git integration')
    git_mutex = git_group.add_mutually_exclusive_group()
    git_mutex.add_argument(
        "--git-only",
        action="store_true",
        help="Only include files tracked by Git (exclude untracked and ignored)"
    )
    git_mutex.add_argument(
        "--git-all",
        action="store_true",
        help="Include Git tracked + untracked files (exclude only ignored)"
    )
    
    # Tree generation
    tree_group = parser.add_argument_group('Tree generation')
    tree_mutex = tree_group.add_mutually_exclusive_group()
    tree_mutex.add_argument(
        "--with-tree", 
        action="store_true", 
        help="Include tree structure using concat configuration"
    )
    tree_mutex.add_argument(
        "--with-tree-full", 
        action="store_true", 
        help="Include full tree with minimal exclusions"
    )
    tree_mutex.add_argument(
        "--with-tree-custom", 
        action="store_true", 
        help="Include tree using custom_tree_files configuration"
    )
    tree_mutex.add_argument(
        "--tree-only", 
        action="store_true", 
        help="Generate only the tree structure (no file contents)"
    )
    
    tree_group.add_argument(
        "--tree-mode",
        choices=['normal', 'full', 'custom'],
        default='normal',
        help="Tree mode for --tree-only (default: normal)"
    )
    
    # Processing options
    process_group = parser.add_argument_group('Processing options')
    process_group.add_argument(
        "--strip-comments", 
        action="store_true", 
        help="Remove comments from code using tree-sitter AST parsing"
    )
    process_group.add_argument(
        "--to-clipboard", 
        action="store_true", 
        help="Copy output to system clipboard (requires X11 on Linux)"
    )
    process_group.add_argument(
        "--no-timestamp", 
        action="store_true", 
        help="Don't add timestamp to output filename"
    )
    
    # Configuration
    config_group = parser.add_argument_group('Configuration')
    config_group.add_argument(
        "--config", 
        help="Path to custom configuration file (default: concat-config.yaml or config.yaml)"
    )
    config_group.add_argument(
        "--mode", 
        choices=['include', 'exclude'],
        help="Override filtering mode from configuration"
    )
    
    # Debug
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug output with detailed filtering information"
    )
    
    # Version
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 2.0.0 (with Git integration and anytree)"
    )
    
    args = parser.parse_args()
    
    # Initialize AIContextCraft
    craft = AIContextCraft(args.config, args.source)
    
    if args.mode:
        craft.config.set_mode(args.mode)
    
    if args.tree_only:
        craft.generate_tree(output_file=args.output, mode=args.tree_mode)
    else:
        tree_mode = 'none'
        if args.with_tree:
            tree_mode = 'normal'
        elif args.with_tree_full:
            tree_mode = 'full'
        elif args.with_tree_custom:
            tree_mode = 'custom'

        git_mode = None
        if args.git_only:
            git_mode = 'tracked'
        elif args.git_all:
            git_mode = 'all'
        
        craft.concat_files(
            output_file=args.output, 
            tree_mode=tree_mode,
            debug=args.debug,
            strip_comments=args.strip_comments,
            no_timestamp=args.no_timestamp,
            to_clipboard=args.to_clipboard,
            git_mode=git_mode
        )

if __name__ == "__main__":
    main()