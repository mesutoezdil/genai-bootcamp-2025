"""
Translate Chinese SRT subtitles to English using Deep Translator.
"""

import os
import re
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from deep_translator import GoogleTranslator
from tqdm import tqdm
import time
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SRTTranslator:
    def __init__(self, source_lang: str = 'zh-CN', target_lang: str = 'en'):
        """
        Initialize the SRT translator.
        
        Args:
            source_lang (str): Source language code (default: 'zh-CN')
            target_lang (str): Target language code (default: 'en')
        """
        try:
            self.translator = GoogleTranslator(source=source_lang, target=target_lang)
            logger.info(f"Initialized translator: {source_lang} -> {target_lang}")
        except Exception as e:
            logger.error(f"Failed to initialize translator: {e}")
            raise

    def _parse_srt(self, content: str) -> List[Dict[str, str]]:
        """
        Parse SRT content into structured format.
        
        Args:
            content (str): Raw SRT file content
            
        Returns:
            List[Dict[str, str]]: List of subtitle entries with index, timing, and text
        """
        entries = []
        current_entry = {}
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            if not line:  # Empty line indicates end of entry
                if current_entry:
                    entries.append(current_entry)
                    current_entry = {}
                continue
                
            if not current_entry:  # Start of new entry
                current_entry = {'index': line}
            elif '-->' in line:  # Timing line
                current_entry['timing'] = line
            elif 'text' not in current_entry:  # First text line
                current_entry['text'] = line
            else:  # Additional text lines
                current_entry['text'] += '\n' + line
                
        if current_entry:  # Add last entry
            entries.append(current_entry)
            
        return entries

    def _translate_text(self, text: str) -> str:
        """
        Translate text with rate limiting and retries.
        
        Args:
            text (str): Text to translate
            
        Returns:
            str: Translated text
        """
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                translated = self.translator.translate(text)
                return translated
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Translation attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    logger.error(f"Translation failed after {max_retries} attempts: {e}")
                    raise

    def translate_srt(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        Translate an SRT file from Chinese to English.
        
        Args:
            input_path (str): Path to input SRT file
            output_path (str, optional): Path to save translated SRT. If None, uses input path with _en.srt suffix
            
        Returns:
            str: Path to the translated SRT file
        """
        try:
            # Input validation
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"SRT file not found: {input_path}")
                
            # Set default output path if not provided
            if output_path is None:
                output_path = str(Path(input_path).with_stem(f"{Path(input_path).stem}_en"))
                
            # Read input file
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse SRT content
            entries = self._parse_srt(content)
            
            # Translate entries
            translated_content = ""
            for entry in tqdm(entries, desc="Translating subtitles"):
                # Keep original index and timing
                translated_content += f"{entry['index']}\n{entry['timing']}\n"
                
                # Translate text
                translated_text = self._translate_text(entry['text'])
                translated_content += f"{translated_text}\n\n"
                
                # Rate limiting
                time.sleep(0.5)  # Avoid hitting rate limits
                
            # Save translated file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
                
            logger.info(f"Translated subtitles saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"SRT translation failed: {e}")
            raise

    def batch_translate(self, input_dir: str, output_dir: Optional[str] = None) -> Dict[str, str]:
        """
        Batch translate multiple SRT files.
        
        Args:
            input_dir (str): Directory containing SRT files
            output_dir (str, optional): Directory to save translated files. If None, uses input_dir
            
        Returns:
            Dict[str, str]: Mapping of input filenames to output paths
        """
        try:
            input_path = Path(input_dir)
            if not input_path.exists():
                raise FileNotFoundError(f"Input directory not found: {input_dir}")
                
            # Set default output directory
            output_path = Path(output_dir) if output_dir else input_path
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Get all SRT files
            srt_files = list(input_path.glob("*.srt"))
            
            if not srt_files:
                logger.warning(f"No SRT files found in {input_dir}")
                return {}
                
            results = {}
            for srt_file in tqdm(srt_files, desc="Processing files"):
                out_file = output_path / f"{srt_file.stem}_en.srt"
                try:
                    translated_path = self.translate_srt(str(srt_file), str(out_file))
                    results[srt_file.name] = translated_path
                except Exception as e:
                    logger.error(f"Failed to translate {srt_file.name}: {e}")
                    results[srt_file.name] = f"Error: {str(e)}"
                    
            return results
            
        except Exception as e:
            logger.error(f"Batch translation failed: {e}")
            raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Translate Chinese SRT files to English")
    parser.add_argument("input", help="Input SRT file or directory")
    parser.add_argument("--output", help="Output file or directory (optional)")
    parser.add_argument("--source", default="zh-CN", help="Source language code (default: zh-CN)")
    parser.add_argument("--target", default="en", help="Target language code (default: en)")
    args = parser.parse_args()
    
    try:
        translator = SRTTranslator(source_lang=args.source, target_lang=args.target)
        
        if os.path.isdir(args.input):
            results = translator.batch_translate(args.input, args.output)
            logger.info(f"Batch translation completed. Processed {len(results)} files.")
        else:
            translated_path = translator.translate_srt(args.input, args.output)
            logger.info(f"Single file translation completed: {translated_path}")
    except Exception as e:
        logger.error(f"Error during translation: {e}")
        sys.exit(1)
