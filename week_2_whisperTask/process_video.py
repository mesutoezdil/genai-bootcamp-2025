import os
import sys
from typing import Optional
import video_utils

def check_file(filepath: str, description: str) -> None:
    """Check if a file exists and raise an error if it doesn't."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{description} not found: {filepath}")

def process_video(
    video_path: str = "chinese.mp4",
    output_path: str = "output.mp4",
    font_size: int = 24,
    font_color: str = "white",
    use_ass: bool = False
) -> None:
    """
    Process a video file: extract audio, transcribe, generate subtitles,
    translate, and embed subtitles back into the video.
    
    Args:
        video_path (str): Path to input video
        output_path (str): Path for output video
        font_size (int): Font size for subtitles
        font_color (str): Font color for subtitles
        use_ass (bool): Whether to use ASS format for subtitles
    """
    try:
        # Check input video exists
        check_file(video_path, "Input video")
        
        # 1. Extract audio if not already done
        audio_path = "audio.mp3"
        if not os.path.exists(audio_path):
            print("1. Extracting audio...")
            if not video_utils.extract_audio(video_path, audio_path):
                raise RuntimeError("Failed to extract audio")
        else:
            print("1. Using existing audio.mp3")
            
        # 2. Generate Chinese transcript
        transcript_path = "transcript_zh.txt"
        if not os.path.exists(transcript_path):
            print("\n2. Generating Chinese transcript...")
            os.system("python transcribe.py")
        else:
            print("\n2. Using existing Chinese transcript")
            
        # 3. Generate Chinese subtitles
        zh_srt_path = "subtitles_zh.srt"
        if not os.path.exists(zh_srt_path):
            print("\n3. Generating Chinese subtitles...")
            os.system("python generate_srt.py")
        else:
            print("\n3. Using existing Chinese subtitles")
            
        # 4. Translate subtitles to English
        en_srt_path = "subtitles_en.srt"
        if not os.path.exists(en_srt_path):
            print("\n4. Translating subtitles to English...")
            os.system("python translate_srt.py")
        else:
            print("\n4. Using existing English subtitles")
            
        # 5. Convert to ASS if requested
        subtitle_path = en_srt_path
        if use_ass:
            print("\n5. Converting subtitles to ASS format...")
            ass_path = "subtitles_en.ass"
            if not video_utils.convert_srt_to_ass(en_srt_path, ass_path):
                raise RuntimeError("Failed to convert subtitles to ASS")
            subtitle_path = ass_path
            
        # 6. Embed subtitles into video
        print(f"\n6. Embedding subtitles into video...")
        if not video_utils.embed_subtitles(
            video_path,
            subtitle_path,
            output_path,
            font_size,
            font_color,
            "ass" if use_ass else "srt"
        ):
            raise RuntimeError("Failed to embed subtitles")
            
        print(f"\n✅ Success! Output video saved as: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main entry point with command line argument handling."""
    from argparse import ArgumentParser
    
    parser = ArgumentParser(description="Process video with subtitles")
    parser.add_argument("--input", default="chinese.mp4", help="Input video file")
    parser.add_argument("--output", default="output.mp4", help="Output video file")
    parser.add_argument("--font-size", type=int, default=24, help="Subtitle font size")
    parser.add_argument("--font-color", default="white", help="Subtitle font color")
    parser.add_argument("--use-ass", action="store_true", help="Use ASS subtitle format")
    
    args = parser.parse_args()
    
    process_video(
        args.input,
        args.output,
        args.font_size,
        args.font_color,
        args.use_ass
    )

if __name__ == "__main__":
    main()
