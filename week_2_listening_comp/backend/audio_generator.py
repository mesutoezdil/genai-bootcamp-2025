import boto3
import json
import os
from typing import Dict, List, Tuple
import tempfile
import subprocess
from datetime import datetime

class ChineseAudioGenerator:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name="us-east-1")
        self.polly = boto3.client('polly')
        self.model_id = "amazon.titan-text-express-v1"  # Changed to a model better for Chinese
        
        # Define Chinese neural voices by gender
        self.voices = {
            'male': ['Zhiwei'],  # Male Mandarin voice
            'female': ['Zhiyu'],  # Female Mandarin voice
            'announcer': 'Zhiwei'  # Default announcer voice
        }
        
        # Create audio output directory
        self.audio_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "frontend/static/audio"
        )
        os.makedirs(self.audio_dir, exist_ok=True)

    def _invoke_bedrock(self, prompt: str) -> str:
        """Invoke Bedrock with the given prompt using Titan model"""
        try:
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "temperature": 0.3,
                        "topP": 0.95,
                        "maxTokens": 2000
                    }
                })
            )
            return json.loads(response['body'].read())['outputText']
        except Exception as e:
            print(f"Error in Bedrock invoke: {str(e)}")
            raise e

    def validate_conversation_parts(self, parts: List[Tuple[str, str, str]]) -> bool:
        """
        Validate that the conversation parts are properly formatted.
        Returns True if valid, False otherwise.
        """
        if not parts:
            print("Error: No conversation parts generated")
            return False
            
        # Check that we have an announcer for intro
        if not parts[0][0].lower() == 'announcer':
            print("Error: First speaker must be Announcer")
            return False
            
        # Check that each part has valid content
        for i, (speaker, text, gender) in enumerate(parts):
            # Check speaker
            if not speaker or not isinstance(speaker, str):
                print(f"Error: Invalid speaker in part {i+1}")
                return False
                
            # Check text
            if not text or not isinstance(text, str):
                print(f"Error: Invalid text in part {i+1}")
                return False
                
            # Check gender
            if gender not in ['male', 'female']:
                print(f"Error: Invalid gender in part {i+1}: {gender}")
                return False
                
            # Check text contains Chinese characters
            if not any('\u4e00' <= c <= '\u9fff' for c in text):
                print(f"Error: Text does not contain Chinese characters in part {i+1}")
                return False
        
        return True

    def parse_conversation(self, question: Dict) -> List[Tuple[str, str, str]]:
        """
        Convert question into a format for audio generation.
        Returns a list of (speaker, text, gender) tuples.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Ask Titan to parse the conversation and assign speakers and genders
                prompt = f"""
                You are a Chinese HSK listening test audio script generator. Format the following question for audio generation.

                Rules:
                1. Introduction and Question parts:
                   - Must start with 'Speaker: Announcer (Gender: male)'
                   - Keep as separate parts

                2. Conversation parts:
                   - Name speakers based on their role (学生, 老师, etc.)
                   - Must specify gender EXACTLY as either 'Gender: male' or 'Gender: female'
                   - Use consistent names for the same speaker
                   - Split long speeches at natural pauses

                Format each part EXACTLY like this, with no variations:
                Speaker: [name] (Gender: male)
                Text: [Chinese text]
                ---

                Example format:
                Speaker: Announcer (Gender: male)
                Text: 请听下面的对话，然后回答问题。
                ---
                Speaker: 学生 (Gender: female)
                Text: 请问这趟火车到北京站吗？
                ---

                Question to format:
                {json.dumps(question, ensure_ascii=False, indent=2)}

                Output ONLY the formatted parts in order: introduction, conversation, question.
                Make sure to specify gender EXACTLY as shown in the example.
                """
                
                response = self._invoke_bedrock(prompt)
                
                # Parse the response into speaker parts
                parts = []
                current_speaker = None
                current_gender = None
                current_text = None
                
                # Track speakers to maintain consistent gender
                speaker_genders = {}
                
                for line in response.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                        
                    if line.startswith('Speaker:'):
                        # Save previous speaker's part if exists
                        if current_speaker and current_text:
                            parts.append((current_speaker, current_text, current_gender))
                        
                        # Parse new speaker and gender
                        try:
                            speaker_part = line.split('Speaker:')[1].strip()
                            current_speaker = speaker_part.split('(')[0].strip()
                            gender_part = speaker_part.split('Gender:')[1].split(')')[0].strip().lower()
                            
                            # Normalize gender
                            if '男' in gender_part or 'male' in gender_part:
                                current_gender = 'male'
                            elif '女' in gender_part or 'female' in gender_part:
                                current_gender = 'female'
                            else:
                                raise ValueError(f"Invalid gender format: {gender_part}")
                            
                            # Check for gender consistency
                            if current_speaker in speaker_genders:
                                current_gender = speaker_genders[current_speaker]
                            else:
                                speaker_genders[current_speaker] = current_gender
                        except Exception as e:
                            print(f"Error parsing speaker/gender: {line}")
                            raise e
                            
                    elif line.startswith('Text:'):
                        current_text = line.split('Text:')[1].strip()
                        
                    elif line == '---' and current_speaker and current_text:
                        parts.append((current_speaker, current_text, current_gender))
                        current_speaker = None
                        current_gender = None
                        current_text = None
                
                # Add final part if exists
                if current_speaker and current_text:
                    parts.append((current_speaker, current_text, current_gender))
                
                # Validate the parsed parts
                if self.validate_conversation_parts(parts):
                    return parts
                    
                print(f"Attempt {attempt + 1}: Invalid conversation format, retrying...")
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise Exception("Failed to parse conversation after multiple attempts")
        
        raise Exception("Failed to generate valid conversation format")

    def get_voice_for_gender(self, gender: str) -> str:
        """Get an appropriate voice for the given gender"""
        if gender == 'male':
            return 'Zhiwei'  # Male Mandarin voice
        else:
            return 'Zhiyu'  # Female Mandarin voice

    def generate_audio_part(self, text: str, voice_name: str) -> str:
        """Generate audio for a single part using Amazon Polly"""
        response = self.polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_name,
            Engine='neural',
            LanguageCode='cmn-CN'  # Changed to Mandarin Chinese
        )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_file.write(response['AudioStream'].read())
            return temp_file.name

    # [Previous methods combine_audio_files, generate_silence remain unchanged]

    def generate_audio(self, question: Dict) -> str:
        """
        Generate audio for the entire question.
        Returns the path to the generated audio file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.audio_dir, f"question_{timestamp}.mp3")
        
        try:
            # Parse conversation into parts
            parts = self.parse_conversation(question)
            
            # Generate audio for each part
            audio_parts = []
            current_section = None
            
            # Generate silence files for pauses
            long_pause = self.generate_silence(2000)  # 2 second pause
            short_pause = self.generate_silence(500)  # 0.5 second pause
            
            for speaker, text, gender in parts:
                # Detect section changes and add appropriate pauses
                if speaker.lower() == 'announcer':
                    if '请听' in text:  # Introduction
                        if current_section is not None:
                            audio_parts.append(long_pause)
                        current_section = 'intro'
                    elif '问题' in text or '选择' in text:  # Question or options
                        audio_parts.append(long_pause)
                        current_section = 'question'
                elif current_section == 'intro':
                    audio_parts.append(long_pause)
                    current_section = 'conversation'
                
                # Get appropriate voice for this speaker
                voice = self.get_voice_for_gender(gender)
                print(f"Using voice {voice} for {speaker} ({gender})")
                
                # Generate audio for this part
                audio_file = self.generate_audio_part(text, voice)
                if not audio_file:
                    raise Exception("Failed to generate audio part")
                audio_parts.append(audio_file)
                
                # Add short pause between conversation turns
                if current_section == 'conversation':
                    audio_parts.append(short_pause)
            
            # Combine all parts into final audio
            if not self.combine_audio_files(audio_parts, output_file):
                raise Exception("Failed to combine audio files")
            
            return output_file
            
        except Exception as e:
            # Clean up the output file if it exists
            if os.path.exists(output_file):
                os.unlink(output_file)
            raise Exception(f"Audio generation failed: {str(e)}")