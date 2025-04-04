import os
import subprocess
from typing import Optional

def extract_audio(video_path: str, audio_path: str) -> bool:
    """
    Extract audio from video file using FFmpeg.
    
    Args:
        video_path (str): Path to input video file
        audio_path (str): Path where audio will be saved
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cmd = [
            "ffmpeg", "-i", video_path,
            "-q:a", "0", "-map", "a",
            "-y",  # Overwrite output file if it exists
            audio_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error extracting audio: {str(e)}")
        return False

def embed_subtitles(
    video_path: str,
    subtitle_path: str,
    output_path: str,
    font_size: int = 24,
    font_color: str = "white",
    subtitle_format: str = "srt"
) -> bool:
    """
    Embed subtitles into video using FFmpeg.
    
    Args:
        video_path (str): Path to input video
        subtitle_path (str): Path to subtitle file
        output_path (str): Path for output video
        font_size (int): Font size for subtitles
        font_color (str): Font color for subtitles
        subtitle_format (str): Format of subtitle file ('srt' or 'ass')
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        filter_params = f"subtitles={subtitle_path}:force_style='FontSize={font_size},PrimaryColour={font_color}'"
        if subtitle_format == "ass":
            filter_params = f"ass={subtitle_path}"
            
        cmd = [
            "ffmpeg", "-i", video_path,
            "-vf", filter_params,
            "-c:v", "libx264", "-c:a", "copy",
            "-y",  # Overwrite output file if it exists
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error embedding subtitles: {str(e)}")
        return False

def convert_srt_to_ass(srt_path: str, ass_path: str) -> bool:
    """
    Convert SRT subtitles to ASS format using FFmpeg.
    
    Args:
        srt_path (str): Path to input SRT file
        ass_path (str): Path where ASS file will be saved
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cmd = ["ffmpeg", "-i", srt_path, "-y", ass_path]
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error converting subtitles: {str(e)}")
        return False
