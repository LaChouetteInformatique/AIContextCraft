# ===== utils/app.py =====

import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# Important : Utilisez des imports relatifs pour les autres modules de utils
from .config_manager import ConfigManager
from .file_processor import FileProcessor
from .tree_generator import TreeGenerator
from .stats_utils import StatsCollector

class AIContextCraft:
    """Main class for AI Context Craft"""
    
    def __init__(self, config_path: str = None, source_dir: str = "."):
        """
        Initializes AIContextCraft
        
        Args:
            config_path: Explicit path to the config file
            source_dir: Source directory to process
        """
        self.source_dir = Path(source_dir).resolve()
        self.config_path = self._find_config_file(config_path)
        self.config = ConfigManager(self.config_path)
        self.processor = FileProcessor(self.config)
        self.tree_gen = TreeGenerator(self.config)
        self.stats = StatsCollector()
        self.logger = None
        
    def _find_config_file(self, explicit_config: Optional[str]) -> str:
        """
        Finds the configuration file to use
        
        Priority order:
        1. Explicitly specified file
        2. concat-config.yaml in the target directory
        3. config.yaml in the target directory
        4. config.yaml in the script's directory
        """
        if explicit_config and Path(explicit_config).exists():
            print(f"📋 Using config: {explicit_config}")
            return explicit_config
        
        target_concat_config = self.source_dir / "concat-config.yaml"
        if target_concat_config.exists():
            print(f"📋 Local config found: {target_concat_config}")
            return str(target_concat_config)
        
        target_config = self.source_dir / "config.yaml"
        if target_config.exists():
            print(f"📋 Local config found: {target_config}")
            return str(target_config)
        
        script_dir = Path(__file__).parent
        default_config = script_dir / "config.yaml"
        if default_config.exists():
            print(f"📋 Default config: {default_config}")
            return str(default_config)
        
        print("⚠️ No config file found, using default values")
        return "config.yaml"
    
    def _setup_logging(self, log_file: Path, debug: bool = False):
        """Configures the logging system with file only."""
        
        # --- FIX: Close old handlers before adding new ones ---
        # This prevents log duplication if the method is called multiple times.
        if self.logger and self.logger.hasHandlers():
            for handler in self.logger.handlers[:]:
                handler.close()
                self.logger.removeHandler(handler)
        # -------------------------------------------------------------------------

        self.logger = logging.getLogger('AIContextCraft')
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        
        self.logger.handlers = []
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # 'w' mode overwrites the log on each run, ensuring a clean log file.
        file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        return self.logger
    
    def _get_output_dir(self, custom_output: Optional[str]) -> Path:
        """
        Determines the output directory
        
        Args:
            custom_output: Custom output path
            
        Returns:
            Path of the output directory
        """
        if custom_output:
            return Path(custom_output).parent
        else:
            return self.source_dir / "build"
        
    def concat_files(self, output_file: str = None, 
                     tree_mode: str = None,
                     debug: bool = False, strip_comments: bool = False,
                     no_timestamp: bool = False):
        """
        Concatenates the project files
        
        Args:
            output_file: Output file
            tree_mode: Tree mode ('none', 'normal', 'full', 'custom')
            debug: Debug mode
            strip_comments: Remove comments
            no_timestamp: Do not add a timestamp
        """
        
        if output_file is None:
            output_dir = self.source_dir / "build"
            if no_timestamp:
                output_file = output_dir / "project_files_concatenated.txt"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = output_dir / f"project_files_{timestamp}.txt"
        else:
            output_file = Path(output_file)
            output_dir = output_file.parent
            
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        log_file = output_file.with_suffix('.log')
        logger = self._setup_logging(log_file, debug)
        
        logger.info("="*60)
        logger.info("🚀 AI Context Craft - Starting")
        logger.info("="*60)
        logger.info(f"📂 Source directory: {self.source_dir}")
        logger.info(f"📋 Config file: {self.config_path}")
        logger.info(f"📄 Output file: {output_file}")
        logger.info(f"📝 Log file: {log_file}")
        logger.info(f"🌳 Tree mode: {tree_mode}")
        logger.info(f"🔧 Options: debug={debug}, strip_comments={strip_comments}")
        logger.info("="*60)
        
        print(f"🚀 Starting concatenation for: {self.source_dir}")
        if tree_mode and tree_mode != 'none':
            print(f"🌳 Tree mode: {tree_mode}")
        print(f"📝 Detailed log in: {log_file}")
        
        self.processor.set_logger(logger)
        result = self.processor.process_directory(
            self.source_dir, 
            debug=debug,
            strip_comments=strip_comments
        )
        
        tree_content = ""
        if tree_mode and tree_mode != 'none':
            print(f"🌳 Generating project tree (mode: {tree_mode})...")
            logger.info(f"\n🌳 Generating project tree (mode: {tree_mode})...")
            tree_content = self.tree_gen.generate_tree(self.source_dir, mode=tree_mode)
            logger.debug(f"Generated tree: {len(tree_content.splitlines())} lines")
        
        self._write_output(output_file, result, tree_content, strip_comments)
        
        logger.info("\n" + "="*60)
        stats_summary = self.stats.get_formatted_summary(result)
        for line in stats_summary.split('\n'):
            logger.info(line)
        
        print("\n" + "="*60)
        print("📊 CONCATENATION SUMMARY")
        print("="*50)
        print(f"📂 Source directory: {result['source_dir']}")
        print(f"📄 Files processed : {result['file_count']}")
        print(f"💾 Total size      : {self._format_size(result['total_size'])}")
        
        estimated_tokens = result['total_size'] // 4
        print(f"📤 Estimated tokens: ~{estimated_tokens:,}")
        
        self.stats.collect_from_result(result)
        if len(self.stats.file_types) > 1:
            print("\n📈 Breakdown by type:")
            sorted_types = sorted(
                self.stats.file_types.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            for ext, count in sorted_types[:5]:
                size = self.stats.file_sizes[ext]
                percentage = (size / result['total_size']) * 100 if result['total_size'] > 0 else 0
                print(f"   {ext:10} : {count:3} files ({self._format_size(size)}, {percentage:.1f}%)")
            
            if len(sorted_types) > 5:
                print(f"   ... and {len(sorted_types) - 5} other types")
        
        print("="*50)
        
        logger.info(f"\n✅ File generated: {output_file}")
        logger.info(f"✅ Full log: {log_file}")
        print(f"\n✅ File generated: {output_file}")
        print(f"📝 Full log: {log_file}")
        
        return str(output_file)
    
    def _format_size(self, size: int) -> str:
        """Formats a size in bytes into a readable format"""
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"
    
    def generate_tree(self, output_file: str = None, mode: str = 'normal'):
        """Generates only the project tree"""
        print(f"🌳 Generating tree for: {self.source_dir}")
        print(f"📋 Mode: {mode}")
        
        if output_file is None:
            output_dir = self.source_dir / "build"
            output_file = output_dir / f"project_tree_{mode}.txt"
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        tree_content = self.tree_gen.generate_tree(self.source_dir, mode=mode)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(tree_content)
        
        print(f"✅ Tree generated: {output_file}")
        return str(output_file)
    
    def _write_output(self, output_file: Path, result: Dict, tree_content: str, strip_comments: bool):
        """Writes the output file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Generated by AI Context Craft\n")
            f.write(f"# Source: {result['source_dir']}\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Files: {result['file_count']}\n")
            f.write(f"# Total size: {result['total_size']:,} bytes\n")
            if strip_comments:
                f.write(f"# Comments: Stripped\n")
            f.write("\n" + "="*60 + "\n\n")
            
            if tree_content:
                f.write("# PROJECT STRUCTURE\n")
                f.write("="*60 + "\n")
                f.write(tree_content)
                f.write("\n" + "="*60 + "\n\n")
            
            f.write("# FILE CONTENTS\n")
            f.write("="*60 + "\n\n")
            for file_data in result['files']:
                f.write(f"\n# ===== {file_data['path']} =====\n\n")
                f.write(file_data['content'])
                f.write("\n")
