import os
from datetime import timedelta
import whisper
import sys

def format_time(seconds: float) -> str:
    """
    Format time in seconds to SRT timestamp format.
    
    Args:
        seconds (float): Time in seconds
        
    Returns:
        str: Formatted time string in SRT format (HH:MM:SS,mmm)
    """
    return str(timedelta(seconds=int(seconds))).replace(".", ",") + "0"

def generate_srt(audio_path: str, output_path: str, language: str = "zh", model_size: str = "small") -> None:
    """
    Generate SRT subtitles from an audio file using Whisper.
    
    Args:
        audio_path (str): Path to the input audio file
        output_path (str): Path where the SRT file will be saved
        language (str): Language code for transcription (default: "zh")
        model_size (str): Size of the Whisper model to use (default: "small")
        
    Raises:
        FileNotFoundError: If the audio file doesn't exist
        RuntimeError: If SRT generation fails
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        print(f"Loading Whisper model ({model_size})...")
        model = whisper.load_model(model_size)
        
        print("Transcribing audio with timestamps...")
        result = model.transcribe(audio_path, language=language)
        
        print("Generating SRT content...")
        srt_content = ""
        for i, segment in enumerate(result["segments"]):
            start = format_time(segment["start"])
            end = format_time(segment["end"])
            text = segment["text"].strip()
            
            srt_content += f"{i+1}\n{start} --> {end}\n{text}\n\n"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(srt_content)
            
        print(f" Subtitles generated: {output_path}")
        
    except Exception as e:
        raise RuntimeError(f"SRT generation failed: {str(e)}")

def main():
    """Main function to run the SRT generation process."""
    audio_path = "audio.mp3"
    output_path = "subtitles_zh.srt"
    
    try:
        generate_srt(audio_path, output_path)
    except Exception as e:
        print(f" Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()