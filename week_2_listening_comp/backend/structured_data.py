from typing import Optional, Dict, List
import boto3
import os
from pypinyin import pinyin, Style
import json
import re

# Model ID for better Chinese support
MODEL_ID = "amazon.titan-text-express-v1"

class ChineseTranscriptStructurer:
    def __init__(self, model_id: str = MODEL_ID):
        """Initialize Bedrock client and Chinese processing"""
        self.bedrock_client = boto3.client('bedrock-runtime', region_name="us-east-1")
        self.model_id = model_id
        self.prompts = {
            1: """Extract questions from section 听力理解1 of this HSK transcript where the answer can be determined solely from the conversation.
            
            ONLY include questions that meet these criteria:
            - The answer can be determined purely from the spoken dialogue
            - Focus on daily conversations and practical situations
            - Clear verbal interactions and responses
            
            For example, INCLUDE questions about:
            - Times and schedules
            - Numbers and quantities
            - Personal preferences
            - Daily activities
            - Simple directions
            
            Format each question exactly like this:

            <question>
            介绍:
            [situation setup in Chinese]
            
            对话:
            [dialogue in Chinese]
            
            问题:
            [question in Chinese]

            选项:
            1. [first option in Chinese]
            2. [second option in Chinese]
            3. [third option in Chinese]
            4. [fourth option in Chinese]
            </question>

            Rules:
            - Only extract questions from the 听力理解1 section
            - Use appropriate HSK level vocabulary and grammar
            - Ignore any practice examples (marked with 例)
            - Do not translate any Chinese text
            - Do not include any section descriptions
            """,
            
            2: """Extract questions from section 听力理解2 of this HSK transcript focusing on extended conversations.
            
            ONLY include questions that meet these criteria:
            - Extended dialogues and conversations
            - Clear context and speaker intentions
            - Natural language flow
            
            For example, INCLUDE questions about:
            - Opinions and preferences
            - Plans and arrangements
            - Personal experiences
            - Work and study situations
            
            Format each question exactly like this:

            <question>
            介绍:
            [situation setup in Chinese]
            
            对话:
            [dialogue in Chinese]
            
            问题:
            [question in Chinese]

            选项:
            1. [first option in Chinese]
            2. [second option in Chinese]
            3. [third option in Chinese]
            4. [fourth option in Chinese]
            </question>

            Rules:
            - Only extract questions from the 听力理解2 section
            - Use natural conversational Chinese
            - Include clear context for each dialogue
            - Do not translate any Chinese text
            """,
            
            3: """Extract questions from section 听力理解3 of this HSK transcript focusing on practical language use.
            
            Format each question exactly like this:

            <question>
            情况:
            [situation in Chinese requiring a response]
            
            问题:
            [question about appropriate response]

            选项:
            1. [first option in Chinese]
            2. [second option in Chinese]
            3. [third option in Chinese]
            4. [fourth option in Chinese]
            </question>

            Rules:
            - Only extract questions from the 听力理解3 section
            - Focus on practical communication scenarios
            - Include clear context for responses
            - Use appropriate HSK level expressions
            """
        }

    def _invoke_bedrock(self, prompt: str, transcript: str) -> Optional[str]:
        """Make a single call to Bedrock with the given prompt"""
        full_prompt = f"{prompt}\n\n转录内容：\n{transcript}"
        
        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "inputText": full_prompt,
                    "textGenerationConfig": {
                        "temperature": 0.1,
                        "topP": 0.9,
                        "maxTokens": 2000
                    }
                })
            )
            return json.loads(response['body'].read())['outputText']
        except Exception as e:
            print(f"调用 Bedrock 时出错: {str(e)}")  # Error invoking Bedrock
            return None

    def _process_chinese_text(self, text: str) -> Dict:
        """Process Chinese text with Pinyin and vocabulary analysis"""
        return {
            'text': text,
            'pinyin': self._generate_pinyin(text),
            'vocabulary': self._extract_vocabulary(text)
        }

    def _generate_pinyin(self, text: str) -> str:
        """Generate Pinyin for Chinese text"""
        try:
            pinyin_list = pinyin(text, style=Style.TONE)
            return ' '.join([item[0] for item in pinyin_list])
        except Exception as e:
            return f"Error generating Pinyin: {str(e)}"

    def _extract_vocabulary(self, text: str) -> List[Dict]:
        """Extract vocabulary items from text"""
        words = list(set(re.findall(r'[\u4e00-\u9fff]+', text)))
        return [
            {
                'word': word,
                'pinyin': self._generate_pinyin(word),
                'length': len(word)
            }
            for word in words if len(word) > 1
        ]

    def structure_transcript(self, transcript: str, hsk_level: int = 4) -> Dict[int, Dict]:
        """Structure the transcript into sections with Chinese language features"""
        results = {}
        for section_num in range(1, 4):
            raw_result = self._invoke_bedrock(self.prompts[section_num], transcript)
            if raw_result:
                # Process the raw text to add Chinese language features
                processed_result = {
                    'content': raw_result,
                    'processed': self._process_chinese_text(raw_result),
                    'metadata': {
                        'section': section_num,
                        'hsk_level': hsk_level
                    }
                }
                results[section_num] = processed_result
        return results

    def save_questions(self, structured_sections: Dict[int, Dict], base_filename: str) -> bool:
        """Save processed sections to files"""
        try:
            # Create questions directory if it doesn't exist
            os.makedirs(os.path.dirname(base_filename), exist_ok=True)
            
            for section_num, content in structured_sections.items():
                # Save full JSON with all features
                json_filename = f"{os.path.splitext(base_filename)[0]}_section{section_num}.json"
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(content, f, ensure_ascii=False, indent=2)

                # Save simple text version with Pinyin
                text_filename = f"{os.path.splitext(base_filename)[0]}_section{section_num}.txt"
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(content['content'])
                    f.write("\n\n拼音 (Pinyin):\n")
                    f.write(content['processed']['pinyin'])
                    f.write("\n\n词汇 (Vocabulary):\n")
                    for word in content['processed']['vocabulary']:
                        f.write(f"{word['word']} ({word['pinyin']})\n")

            return True
        except Exception as e:
            print(f"保存问题时出错: {str(e)}")  # Error saving questions
            return False

    def load_transcript(self, filename: str) -> Optional[str]:
        """Load transcript from a file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"加载转录时出错: {str(e)}")  # Error loading transcript
            return None

if __name__ == "__main__":
    structurer = ChineseTranscriptStructurer()
    transcript = structurer.load_transcript("backend/data/transcripts/sY7L5cfCWno.txt")
    if transcript:
        structured_sections = structurer.structure_transcript(transcript, hsk_level=4)
        structurer.save_questions(structured_sections, "backend/data/questions/sY7L5cfCWno.txt")