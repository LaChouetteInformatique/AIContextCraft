"""Utilities for statistics"""
from typing import Dict, Any
from collections import defaultdict
from pathlib import Path
from .token_estimator import TokenEstimator

class StatsCollector:
    """Collects and displays statistics"""
    
    def __init__(self):
        self.stats = defaultdict(int)
        self.file_types = defaultdict(int)
        self.file_sizes = defaultdict(int)
        self.token_estimator = TokenEstimator()
    
    def collect_from_result(self, result: Dict[str, Any]):
        """Collects statistics from the processing result"""
        self.stats['total_files'] = result['file_count']
        self.stats['total_size'] = result['total_size']
        
        # --- FIX: Reset stats by type before collecting ---
        self.file_types.clear()
        self.file_sizes.clear()
        # ----------------------------------------------------------------------
        
        # Analyze by file type
        for file_data in result['files']:
            ext = Path(file_data['path']).suffix or '.none' # Use .none for files without an extension
            self.file_types[ext] += 1
            self.file_sizes[ext] += file_data['size']
    
    def get_formatted_summary(self, result: Dict[str, Any]) -> str:
        """
        Returns a formatted summary for the logs
        
        Returns:
            String with the complete summary
        """
        self.collect_from_result(result)
        
        lines = []
        lines.append("📊 CONCATENATION SUMMARY")
        lines.append("="*50)
        lines.append(f"📂 Source directory: {result['source_dir']}")
        lines.append(f"📄 Files processed : {self.stats['total_files']}")
        lines.append(f"💾 Total size      : {self._format_size(self.stats['total_size'])}")
        
        # Token estimation
        estimated_tokens = self.stats['total_size'] // 4
        lines.append(f"🔤 Estimated tokens: ~{estimated_tokens:,}")

        
        # 🆕 Improved token estimate
        if hasattr(self, 'token_estimator'):
            # Get all content for better estimate
            total_content = "\n".join([f['content'] for f in result['files']])
            estimation = self.token_estimator.estimate_tokens(total_content)
            lines.append("")
            lines.append(self.token_estimator.format_summary(estimation, include_models=False))
        else:
            if result['files']:
                total_content = "\n".join([f['content'] for f in result['files']])
                estimation = self.token_estimator.estimate_tokens(total_content)
                lines.append("")
                lines.append(self.token_estimator.format_summary(estimation, include_models=False))
            else:
                # Fallback for empty results
                lines.append(f"🔤 No content to estimate")

        # Breakdown by type if more than one type
        if len(self.file_types) > 1:
            lines.append("\n📈 Breakdown by type:")
            
            sorted_types = sorted(
                self.file_types.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            for ext, count in sorted_types[:10]:
                size = self.file_sizes[ext]
                percentage = (size / self.stats['total_size']) * 100 if self.stats['total_size'] > 0 else 0
                lines.append(f"   {ext:10} : {count:3} files ({self._format_size(size)}, {percentage:.1f}%)")
            
            if len(sorted_types) > 10:
                lines.append(f"   ... and {len(sorted_types) - 10} other types")
        
        # Errors if present
        if 'errors' in result and result['errors']:
            lines.append(f"\n⚠️ Errors: {len(result['errors'])}")
            for error in result['errors'][:5]:
                lines.append(f"   - {error}")
            if len(result['errors']) > 5:
                lines.append(f"   ... and {len(result['errors']) - 5} other errors")
        
        lines.append("="*50)
        
        return '\n'.join(lines)

    def display_summary(self, result: Dict[str, Any]):
        """Displays a detailed summary on the console"""
        summary = self.get_formatted_summary(result)
        print("\n" + summary)
    
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
    
    def get_stats(self) -> Dict[str, Any]:
        """Returns the collected statistics"""
        return {
            'total_files': self.stats['total_files'],
            'total_size': self.stats['total_size'],
            'file_types': dict(self.file_types),
            'file_sizes': dict(self.file_sizes),
            'estimated_tokens': self.stats['total_size'] // 4
        }
    
    def reset(self):
        """Resets the statistics"""
        self.stats.clear()
        self.file_types.clear()
        self.file_sizes.clear()
    
    def add_custom_stat(self, key: str, value: Any):
        """Adds a custom statistic"""
        self.stats[key] = value
    
    def format_for_header(self) -> str:
        """Formats the stats for the output file header"""
        lines = []
        lines.append(f"# Files: {self.stats.get('total_files', 0)}")
        lines.append(f"# Total size: {self.stats.get('total_size', 0):,} bytes")
        lines.append(f"# Estimated tokens: ~{self.stats.get('total_size', 0) // 4:,}")
        
        if self.file_types:
            top_types = sorted(self.file_types.items(), key=lambda x: x[1], reverse=True)[:3]
            types_str = ", ".join([f"{ext}({count})" for ext, count in top_types])
            lines.append(f"# Main types: {types_str}")
        
        return "\n".join(lines)