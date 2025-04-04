import os
import whisper
import sys

def check_file_exists(filepath: str) -> bool:
    """
    Check if a file exists at the given path.
    
    Args:
        filepath (str): Path to the file to check
        
    Returns:
        bool: True if file exists, False otherwise
    """
    return os.path.exists(filepath)

def transcribe_audio(audio_path: str, output_path: str, model_size: str = "small") -> None:
    """
    Transcribe audio file to text using Whisper model.
    
    Args:
        audio_path (str): Path to the input audio file
        output_path (str): Path where the transcript will be saved
        model_size (str): Size of the Whisper model to use (default: "small")
    
    Raises:
        FileNotFoundError: If the audio file doesn't exist
        RuntimeError: If transcription fails
    """
    if not check_file_exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        print(f"Loading Whisper model ({model_size})...")
        model = whisper.load_model(model_size)
        
        print("Transcribing audio...")
        result = model.transcribe(audio_path, language="zh")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
            
        print(f" Chinese transcription completed. Saved as {output_path}")
        
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {str(e)}")

def main():
    """Main function to run the transcription process."""
    audio_path = "audio.mp3"
    output_path = "transcript_zh.txt"
    
    try:
        transcribe_audio(audio_path, output_path)
    except Exception as e:
        print(f" Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
