import os
from deep_translator import GoogleTranslator
import re
import sys
from typing import List, Tuple

def parse_srt_line(line: str) -> Tuple[bool, bool]:
    """
    Parse a line from an SRT file to determine its type.
    
    Args:
        line (str): A line from the SRT file
        
    Returns:
        Tuple[bool, bool]: (is_timestamp, is_blank)
    """
    line = line.strip()
    is_timestamp = "-->" in line
    is_blank = len(line) == 0 or re.match(r"^\d+$", line) is not None
    return is_timestamp, is_blank

def translate_srt(input_path: str, output_path: str, source_lang: str = "zh-CN", target_lang: str = "en") -> None:
    """
    Translate an SRT subtitle file from one language to another.
    
    Args:
        input_path (str): Path to the input SRT file
        output_path (str): Path where the translated SRT file will be saved
        source_lang (str): Source language code (default: "zh-CN")
        target_lang (str): Target language code (default: "en")
        
    Raises:
        FileNotFoundError: If the input SRT file doesn't exist
        RuntimeError: If translation fails
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input SRT file not found: {input_path}")

    try:
        print(f"Initializing translator ({source_lang} -> {target_lang})...")
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        
        print("Reading SRT file...")
        with open(input_path, "r", encoding="utf-8") as f:
            srt_content = f.readlines()
        
        print("Translating subtitles...")
        translated_srt: List[str] = []
        for line in srt_content:
            is_timestamp, is_blank = parse_srt_line(line)
            
            if is_timestamp or is_blank:
                translated_srt.append(line)
            else:
                translated_text = translator.translate(line.strip())
                translated_srt.append(translated_text + "\n")
        
        print("Saving translated subtitles...")
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(translated_srt)
            
        print(f"✅ Translated subtitles generated: {output_path}")
        
    except Exception as e:
        raise RuntimeError(f"Translation failed: {str(e)}")

def main():
    """Main function to run the SRT translation process."""
    input_path = "subtitles_zh.srt"
    output_path = "subtitles_en.srt"
    
    try:
        translate_srt(input_path, output_path)
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
