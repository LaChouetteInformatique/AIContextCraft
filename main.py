# ===== main.py =====

#!/usr/bin/env python3
"""
AI Context Craft - Main Module
Tool for preparing code context for LLMs
"""

import sys
import argparse
from pathlib import Path

# Cette ligne est maintenant la clé : elle permet de trouver le package utils
sys.path.append(str(Path(__file__).parent))

# Importez la classe depuis son nouvel emplacement
from utils.app import AIContextCraft

def main():
    """Main entry point""" 
    parser = argparse.ArgumentParser(
        description="AI Context Craft - Prepare your code for LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "source", 
        nargs='?',
        default=".",
        help="Source directory to process (default: current directory)"
    )
    
    parser.add_argument("-o", "--output", help="Output file")
    
    tree_group = parser.add_mutually_exclusive_group()
    tree_group.add_argument(
        "--with-tree", 
        action="store_true", 
        help="Include tree with the same configuration as concatenation"
    )
    tree_group.add_argument(
        "--with-tree-full", 
        action="store_true", 
        help="Include full tree (uses tree_project_files if available)"
    )
    tree_group.add_argument(
        "--with-tree-custom", 
        action="store_true", 
        help="Include custom tree (uses custom_tree_files if available)"
    )
    tree_group.add_argument(
        "--tree-only", 
        action="store_true", 
        help="Generate only the tree (no concatenation)"
    )
    
    parser.add_argument(
        "--tree-mode",
        choices=['normal', 'full', 'custom'],
        default='normal',
        help="Tree mode for --tree-only (default: normal)"
    )
    
    parser.add_argument(
        "--strip-comments", 
        action="store_true", 
        help="Remove comments from the code"
    )
    parser.add_argument(
        "--no-timestamp", 
        action="store_true", 
        help="Do not add a timestamp to the filename"
    )
    
    parser.add_argument(
        "--config", 
        help="Custom configuration file"
    )
    parser.add_argument(
        "--mode", 
        choices=['include', 'exclude'],
        help="Force the filtering mode"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Debug mode with detailed information"
    )
    
    args = parser.parse_args()
    
    # On instancie la classe importée
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
        
        craft.concat_files(
            output_file=args.output, 
            tree_mode=tree_mode,
            debug=args.debug,
            strip_comments=args.strip_comments,
            no_timestamp=args.no_timestamp
        )

if __name__ == "__main__":
    main()