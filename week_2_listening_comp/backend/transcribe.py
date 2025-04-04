"""
Transcribe Chinese audio to text using Whisper.
"""

import whisper
import os
import logging
from pathlib import Path
from typing import Optional, Dict
from tqdm import tqdm
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChineseTranscriber:
    def __init__(self, model_size: str = "medium"):
        """
        Initialize the transcriber with specified Whisper model size.
        
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

    def transcribe_audio(self, audio_path: str, output_path: Optional[str] = None) -> Dict:
        """
        Transcribe Chinese audio file to text.
        
        Args:
            audio_path (str): Path to the input audio file
            output_path (str, optional): Path to save the transcript. If None, will use input path with .txt extension
            
        Returns:
            Dict: Whisper transcription result containing text and other metadata
        """
        try:
            # Input validation
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
                
            # Set default output path if not provided
            if output_path is None:
                output_path = str(Path(audio_path).with_suffix('.txt'))
                
            logger.info(f"Transcribing {audio_path}")
            
            # Transcribe with progress bar
            with tqdm(total=100, desc="Transcribing") as pbar:
                result = self.model.transcribe(
                    audio_path,
                    language="zh",
                    task="transcribe",
                    fp16=False  # Use float32 for better accuracy
                )
                pbar.update(100)
                
            # Save transcript
            if result and result.get('text'):
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result['text'])
                logger.info(f"Transcript saved to {output_path}")
            else:
                raise ValueError("No transcription text generated")
                
            return result
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

    def batch_transcribe(self, input_dir: str, output_dir: Optional[str] = None) -> Dict[str, Dict]:
        """
        Batch transcribe multiple audio files in a directory.
        
        Args:
            input_dir (str): Directory containing audio files
            output_dir (str, optional): Directory to save transcripts. If None, uses input_dir
            
        Returns:
            Dict[str, Dict]: Mapping of filenames to their transcription results
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
                out_file = output_path / f"{audio_file.stem}_transcript.txt"
                try:
                    result = self.transcribe_audio(str(audio_file), str(out_file))
                    results[audio_file.name] = result
                except Exception as e:
                    logger.error(f"Failed to transcribe {audio_file.name}: {e}")
                    results[audio_file.name] = {"error": str(e)}
                    
            return results
            
        except Exception as e:
            logger.error(f"Batch transcription failed: {e}")
            raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Transcribe Chinese audio files using Whisper")
    parser.add_argument("input", help="Input audio file or directory")
    parser.add_argument("--output", help="Output file or directory (optional)")
    parser.add_argument("--model", default="medium", help="Whisper model size (default: medium)")
    args = parser.parse_args()
    
    try:
        transcriber = ChineseTranscriber(model_size=args.model)
        
        if os.path.isdir(args.input):
            results = transcriber.batch_transcribe(args.input, args.output)
            logger.info(f"Batch transcription completed. Processed {len(results)} files.")
        else:
            result = transcriber.transcribe_audio(args.input, args.output)
            logger.info("Single file transcription completed.")
    except Exception as e:
        logger.error(f"Error during transcription: {e}")
        sys.exit(1)
