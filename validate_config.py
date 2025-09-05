#!/usr/bin/env python3
"""Configuration validation"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from utils.config_manager import ConfigManager
from utils.pattern_matcher import PatternMatcher

def validate_configuration(config_path: str = "config.yaml"):
    """Validates the configuration and provides suggestions"""
    
    print("🔍 CONFIGURATION VALIDATION")
    print("=" * 50)
    
    try:
        # Load the config
        config_mgr = ConfigManager(config_path)
        print(f"📋 Configuration file: {config_path}")
        print(f"📄 Detected format: {config_mgr.config_format.upper()}")
        
        if config_mgr.is_advanced_format():
            # Validate the advanced configuration
            concat_config = config_mgr.get_concat_config()
            tree_config = config_mgr.get_tree_config(mode='full')
            
            print("\n📦 Concatenation configuration:")
            print(f"  Mode: {concat_config.get('mode', 'not set')}")
            print(f"  Inclusion patterns: {len(concat_config.get('include', []))}")
            print(f"  Exclusion patterns: {len(concat_config.get('exclude', []))}")
            
            if 'tree_project_files' in config_mgr.config:
                print("\n🌳 Tree configuration (separate):")
                print(f"  Mode: {tree_config.get('mode', 'not set')}")
                print(f"  Exclusion patterns: {len(tree_config.get('exclude', []))}")
            else:
                print("\n🌳 Tree configuration: Uses concatenation config")
            
            # Validate the patterns
            matcher = PatternMatcher(config_mgr)
            all_patterns = []
            all_patterns.extend(concat_config.get('include', []))
            all_patterns.extend(concat_config.get('exclude', []))
            
            errors = []
            warnings = []
            
            for pattern in all_patterns:
                if not pattern or pattern.isspace():
                    warnings.append(f"Empty pattern detected")
                elif pattern.startswith(' ') or pattern.endswith(' '):
                    warnings.append(f"Pattern with spaces: '{pattern}'")
            
            if errors:
                print("\n❌ Validation errors:")
                for error in errors:
                    print(f"  • {error}")
            
            if warnings:
                print("\n⚠️  Warnings:")
                for warning in warnings:
                    print(f"  • {warning}")
            
            if not errors and not warnings:
                print("\n✅ Valid configuration!")
            
        else:
            print("\n📝 Legacy configuration detected")
            print(f"  Included extensions: {len(config_mgr.config.get('include_extensions', []))}")
            print(f"  Excluded directories: {len(config_mgr.config.get('exclude_dirs', []))}")
            print("\n💡 Tip: Consider the advanced format for more flexibility")
        
        print("\n✨ IMPROVEMENT SUGGESTIONS:")
        print("  • Use --with-tree to include the tree in the output")
        print("  • Use --strip-comments to save tokens")
        print("  • Use --debug to understand the filtering")
        print("  • Use --with-full-tree for a complete tree with filtered content")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during validation: {e}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validate the configuration")
    parser.add_argument("--config", default="config.yaml", help="Configuration file")
    args = parser.parse_args()
    
    success = validate_configuration(args.config)
    sys.exit(0 if success else 1)