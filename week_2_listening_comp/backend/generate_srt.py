"""
Generate SRT subtitles from audio using Whisper.
"""

import whisper
import os
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import timedelta
from tqdm import tqdm
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SubtitleGenerator:
    def __init__(self, model_size: str = "medium"):
        """
        Initialize the subtitle generator with specified Whisper model size.
        
        Args:
            model_size (str): Size of the Whisper model to use ('tiny', 'base', 'small', 'medium', 'large')
        """
        try:
            logger.info(f"Loading Whisper model: {model_size}")
            self.model = whisper.load_model(model_size)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise

    def _format_timestamp(self, seconds: float) -> str:
        """
        Convert seconds to SRT timestamp format (HH:MM:SS,mmm).
        
        Args:
            seconds (float): Time in seconds
            
        Returns:
            str: Formatted timestamp
        """
        td = timedelta(seconds=seconds)
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        seconds = td.seconds % 60
        milliseconds = round(td.microseconds / 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    def _create_subtitle_entry(self, index: int, segment: Dict) -> str:
        """
        Create a single SRT subtitle entry.
        
        Args:
            index (int): Subtitle index number
            segment (Dict): Segment data from Whisper
            
        Returns:
            str: Formatted SRT entry
        """
        start_time = self._format_timestamp(segment['start'])
        end_time = self._format_timestamp(segment['end'])
        text = segment['text'].strip()
        
        return f"{index}\n{start_time} --> {end_time}\n{text}\n\n"

    def generate_srt(self, audio_path: str, output_path: Optional[str] = None) -> str:
        """
        Generate SRT subtitles for an audio file.
        
        Args:
            audio_path (str): Path to the input audio file
            output_path (str, optional): Path to save the SRT file. If None, will use input path with .srt extension
            
        Returns:
            str: Path to the generated SRT file
        """
        try:
            # Input validation
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
                
            # Set default output path if not provided
            if output_path is None:
                output_path = str(Path(audio_path).with_suffix('.srt'))
                
            logger.info(f"Generating subtitles for {audio_path}")
            
            # Transcribe with progress bar
            with tqdm(total=100, desc="Transcribing") as pbar:
                result = self.model.transcribe(
                    audio_path,
                    language="zh",
                    task="transcribe",
                    fp16=False
                )
                pbar.update(100)
                
            # Generate SRT content
            srt_content = ""
            for i, segment in enumerate(result['segments'], 1):
                srt_content += self._create_subtitle_entry(i, segment)
                
            # Save SRT file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
                
            logger.info(f"Subtitles saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"SRT generation failed: {e}")
            raise

    def batch_generate_srt(self, input_dir: str, output_dir: Optional[str] = None) -> Dict[str, str]:
        """
        Batch generate SRT files for multiple audio files.
        
        Args:
            input_dir (str): Directory containing audio files
            output_dir (str, optional): Directory to save SRT files. If None, uses input_dir
            
        Returns:
            Dict[str, str]: Mapping of input filenames to output SRT paths
        """
        try:
            input_path = Path(input_dir)
            if not input_path.exists():
                raise FileNotFoundError(f"Input directory not found: {input_dir}")
                
            # Set default output directory
            output_path = Path(output_dir) if output_dir else input_path
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Get all audio files
            audio_files = [
                f for f in input_path.glob("*")
                if f.suffix.lower() in ['.mp3', '.wav', '.m4a', '.flac']
            ]
            
            if not audio_files:
                logger.warning(f"No audio files found in {input_dir}")
                return {}
                
            results = {}
            for audio_file in tqdm(audio_files, desc="Processing files"):
                out_file = output_path / f"{audio_file.stem}.srt"
                try:
                    srt_path = self.generate_srt(str(audio_file), str(out_file))
                    results[audio_file.name] = srt_path
                except Exception as e:
                    logger.error(f"Failed to generate SRT for {audio_file.name}: {e}")
                    results[audio_file.name] = f"Error: {str(e)}"
                    
            return results
            
        except Exception as e:
            logger.error(f"Batch SRT generation failed: {e}")
            raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate SRT subtitles from audio files using Whisper")
    parser.add_argument("input", help="Input audio file or directory")
    parser.add_argument("--output", help="Output file or directory (optional)")
    parser.add_argument("--model", default="medium", help="Whisper model size (default: medium)")
    args = parser.parse_args()
    
    try:
        generator = SubtitleGenerator(model_size=args.model)
        
        if os.path.isdir(args.input):
            results = generator.batch_generate_srt(args.input, args.output)
            logger.info(f"Batch SRT generation completed. Processed {len(results)} files.")
        else:
            srt_path = generator.generate_srt(args.input, args.output)
            logger.info(f"Single file SRT generation completed: {srt_path}")
    except Exception as e:
        logger.error(f"Error during SRT generation: {e}")
        sys.exit(1)
