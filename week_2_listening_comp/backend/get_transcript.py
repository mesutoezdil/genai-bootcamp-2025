from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional, List, Dict
import os
from pypinyin import pinyin, Style
import json
import re

class ChineseTranscriptDownloader:
    def __init__(self, languages: List[str] = ["zh", "zh-Hans", "zh-CN", "en"]):
        """Initialize with Chinese language preferences"""
        self.languages = languages
        self.transcript_dir = "./transcripts"
        os.makedirs(self.transcript_dir, exist_ok=True)

    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL
        
        Args:
            url (str): YouTube URL
            
        Returns:
            Optional[str]: Video ID if found, None otherwise
        """
        if "v=" in url:
            return url.split("v=")[1].split("&")[0][:11]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1][:11]
        return None

    def get_transcript(self, video_id: str) -> Optional[Dict]:
        """
        Download YouTube Transcript with enhanced Chinese processing
        
        Args:
            video_id (str): YouTube video ID or URL
            
        Returns:
            Optional[Dict]: Transcript with Chinese processing if successful
        """
        # Extract video ID if full URL is provided
        if "youtube.com" in video_id or "youtu.be" in video_id:
            video_id = self.extract_video_id(video_id)
            
        if not video_id:
            print("无效的视频ID或URL")  # Invalid video ID or URL
            return None

        print(f"正在下载视频字幕 (ID: {video_id})")  # Downloading transcript
        
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=self.languages)
            return self._process_chinese_transcript(transcript)
        except Exception as e:
            print(f"发生错误: {str(e)}")  # An error occurred
            return None

    def _process_chinese_transcript(self, transcript: List[Dict]) -> Dict:
        """
        Process transcript with Chinese language features
        
        Args:
            transcript (List[Dict]): Raw transcript data
            
        Returns:
            Dict: Processed transcript with Chinese features
        """
        processed_entries = []
        
        for entry in transcript:
            text = entry['text']
            
            # Extract Chinese characters
            chinese_text = self._extract_chinese_text(text)
            
            if chinese_text:
                processed_entry = {
                    'text': text,
                    'chinese_only': chinese_text,
                    'pinyin': self._generate_pinyin(chinese_text),
                    'start': entry['start'],
                    'duration': entry['duration'],
                    'vocabulary': self._extract_vocabulary(chinese_text)
                }
                processed_entries.append(processed_entry)

        return {
            'entries': processed_entries,
            'metadata': {
                'total_entries': len(processed_entries),
                'total_duration': sum(entry['duration'] for entry in processed_entries),
                'vocabulary_summary': self._generate_vocabulary_summary(processed_entries)
            }
        }

    def _extract_chinese_text(self, text: str) -> str:
        """Extract Chinese characters from text"""
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
        chinese_chars = chinese_pattern.findall(text)
        return ' '.join(chinese_chars)

    def _generate_pinyin(self, text: str) -> str:
        """Generate Pinyin for Chinese text"""
        try:
            pinyin_list = pinyin(text, style=Style.TONE)
            return ' '.join([item[0] for item in pinyin_list])
        except Exception as e:
            return f"Error generating Pinyin: {str(e)}"

    def _extract_vocabulary(self, text: str) -> List[Dict]:
        """Extract vocabulary items from text"""
        words = list(set(text.split()))
        return [
            {
                'word': word,
                'pinyin': self._generate_pinyin(word),
                'length': len(word)
            }
            for word in words if len(word) > 1  # Only include multi-character words
        ]

    def _generate_vocabulary_summary(self, entries: List[Dict]) -> Dict:
        """Generate vocabulary summary from all entries"""
        all_vocab = {}
        for entry in entries:
            for vocab in entry['vocabulary']:
                word = vocab['word']
                if word not in all_vocab:
                    all_vocab[word] = {
                        'pinyin': vocab['pinyin'],
                        'frequency': 1,
                        'length': vocab['length']
                    }
                else:
                    all_vocab[word]['frequency'] += 1
        
        return all_vocab

    def save_transcript(self, transcript: Dict, filename: str) -> bool:
        """
        Save processed transcript to files
        
        Args:
            transcript (Dict): Processed transcript data
            filename (str): Base filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Save full transcript with all features
            full_path = os.path.join(self.transcript_dir, f"{filename}_full.json")
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(transcript, f, ensure_ascii=False, indent=2)

            # Save simple text version
            text_path = os.path.join(self.transcript_dir, f"{filename}_text.txt")
            with open(text_path, 'w', encoding='utf-8') as f:
                for entry in transcript['entries']:
                    f.write(f"{entry['chinese_only']}\n")
                    f.write(f"拼音: {entry['pinyin']}\n\n")

            # Save vocabulary list
            vocab_path = os.path.join(self.transcript_dir, f"{filename}_vocabulary.txt")
            with open(vocab_path, 'w', encoding='utf-8') as f:
                f.write("词汇表 (Vocabulary List):\n\n")
                for word, info in transcript['metadata']['vocabulary_summary'].items():
                    f.write(f"词语 (Word): {word}\n")
                    f.write(f"拼音 (Pinyin): {info['pinyin']}\n")
                    f.write(f"出现频率 (Frequency): {info['frequency']}\n\n")

            return True
        except Exception as e:
            print(f"保存字幕时出错: {str(e)}")  # Error saving transcript
            return False

def main(video_url: str, print_transcript: bool = False):
    # Initialize downloader
    downloader = ChineseTranscriptDownloader()
    
    # Get and process transcript
    transcript = downloader.get_transcript(video_url)
    
    if transcript:
        # Save transcript
        video_id = downloader.extract_video_id(video_url)
        if downloader.save_transcript(transcript, video_id):
            print(f"字幕已成功保存 (Saved to {video_id}_*.json/txt)")
            
            if print_transcript:
                print("\n字幕内容 (Transcript Content):")
                for entry in transcript['entries']:
                    print(f"中文: {entry['chinese_only']}")
                    print(f"拼音: {entry['pinyin']}")
                    print("---")
        else:
            print("保存字幕失败")  # Failed to save transcript
    else:
        print("获取字幕失败")  # Failed to get transcript

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=sY7L5cfCWno&list=PLkGU7DnOLgRMl-h4NxxrGbK-UdZHIXzKQ"
    main(video_url, print_transcript=True)