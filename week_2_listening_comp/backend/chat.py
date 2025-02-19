# chinese_language_assistant.py
import boto3
import streamlit as st
from typing import Optional, Dict, Any, List
import json
from pypinyin import pinyin, Style
import re

# Model ID for Chinese language processing
MODEL_ID = "amazon.titan-text-express-v1"

class ChineseLanguageAssistant:
    def __init__(self, model_id: str = MODEL_ID):
        """Initialize Chinese language assistant"""
        self.bedrock_client = boto3.client('bedrock-runtime', region_name="us-east-1")
        self.model_id = model_id
        
        # HSK vocabulary levels
        self.hsk_levels = {
            1: "基础词汇",  # Basic vocabulary
            2: "初级词汇",  # Elementary vocabulary
            3: "中级词汇",  # Intermediate vocabulary
            4: "中高级词汇", # Upper-intermediate vocabulary
            5: "高级词汇",  # Advanced vocabulary
            6: "高等词汇"   # Superior vocabulary
        }

    def generate_response(self, message: str, context: Optional[Dict] = None) -> Optional[Dict]:
        """Generate a response using Amazon Bedrock with Chinese language focus"""
        if context is None:
            context = {"mode": "general", "hsk_level": 3}

        # Prepare the prompt based on the context
        prompt = self._prepare_prompt(message, context)

        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "temperature": 0.7,
                        "topP": 0.9,
                        "maxTokens": 1000,
                        "stopSequences": ["User:", "用户："]
                    }
                })
            )
            
            response_text = json.loads(response['body'].read())['outputText']
            return self._process_response(response_text, context)
            
        except Exception as e:
            st.error(f"生成回答时出错: {str(e)}")  # Error generating response
            return None

    def _prepare_prompt(self, message: str, context: Dict) -> str:
        """Prepare the prompt based on the context and mode"""
        mode = context.get("mode", "general")
        hsk_level = context.get("hsk_level", 3)
        
        base_prompt = f"""You are a Chinese language teaching assistant. 
Respond in Chinese (with English translations when needed).
Current HSK level: {hsk_level}

Instructions:
- Use vocabulary appropriate for HSK level {hsk_level}
- Include Pinyin for difficult words
- Explain grammar points when relevant
- Correct any Chinese language errors in user input

User message: {message}

Response (format as JSON):
"""

        mode_specific_prompts = {
            "grammar": "Focus on explaining Chinese grammar patterns and usage.",
            "vocabulary": "Focus on vocabulary explanation with examples.",
            "conversation": "Focus on natural conversation practice.",
            "correction": "Focus on correcting Chinese language errors.",
            "listening": "Focus on listening comprehension practice."
        }

        if mode in mode_specific_prompts:
            base_prompt = f"{base_prompt}\nMode: {mode_specific_prompts[mode]}"

        return base_prompt

    def _process_response(self, response_text: str, context: Dict) -> Dict:
        """Process and structure the response with additional language learning features"""
        try:
            # Extract or prepare components
            chinese_text = self._extract_chinese(response_text)
            pinyin_text = self.generate_pinyin(chinese_text)
            key_vocab = self._extract_key_vocabulary(chinese_text, context.get("hsk_level", 3))
            
            return {
                "chinese": chinese_text,
                "pinyin": pinyin_text,
                "key_vocabulary": key_vocab,
                "full_response": response_text
            }
        except Exception as e:
            st.error(f"处理回答时出错: {str(e)}")  # Error processing response
            return {"error": str(e)}

    def generate_pinyin(self, text: str) -> str:
        """Generate Pinyin for Chinese text"""
        try:
            pinyin_list = pinyin(text, style=Style.TONE)
            return ' '.join([item[0] for item in pinyin_list])
        except Exception as e:
            return f"Error generating Pinyin: {str(e)}"

    def _extract_chinese(self, text: str) -> str:
        """Extract Chinese characters from text"""
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
        chinese_chars = chinese_pattern.findall(text)
        return ' '.join(chinese_chars)

    def _extract_key_vocabulary(self, text: str, hsk_level: int) -> List[Dict]:
        """Extract and explain key vocabulary based on HSK level"""
        # This would typically connect to a HSK vocabulary database
        # For now, we'll return a basic structure
        words = list(set(text.split()))
        vocab_list = []
        
        for word in words:
            if len(word) > 1:  # Only process words, not single characters
                vocab_list.append({
                    "word": word,
                    "pinyin": self.generate_pinyin(word),
                    "hsk_level": min(self._estimate_hsk_level(word), hsk_level),
                    "english": "Translation placeholder"  # Would connect to translation service
                })
        
        return vocab_list

    def _estimate_hsk_level(self, word: str) -> int:
        """Estimate HSK level of a word (placeholder implementation)"""
        # This would typically connect to a HSK vocabulary database
        return min(len(word) + 1, 6)  # Simple placeholder logic

    def get_grammar_explanation(self, text: str) -> str:
        """Get grammar explanation for Chinese text"""
        prompt = f"""Explain the grammar patterns in this Chinese text:
        {text}
        
        Focus on:
        1. Sentence structure
        2. Particle usage
        3. Common patterns
        """
        
        return self.generate_response(prompt, {"mode": "grammar"})

    def practice_conversation(self, topic: str, hsk_level: int) -> Dict:
        """Generate a practice conversation on a given topic"""
        prompt = f"""Create a short Chinese conversation about {topic} suitable for HSK level {hsk_level}.
        Include:
        1. Natural dialogue
        2. Common expressions
        3. Level-appropriate vocabulary
        """
        
        return self.generate_response(prompt, {
            "mode": "conversation",
            "hsk_level": hsk_level
        })


if __name__ == "__main__":
    assistant = ChineseLanguageAssistant()
    st.title("中文学习助手 - Chinese Learning Assistant")
    
    # Session state initialization
    if 'hsk_level' not in st.session_state:
        st.session_state.hsk_level = 3
    
    # Sidebar for settings
    with st.sidebar:
        st.session_state.hsk_level = st.slider("HSK Level", 1, 6, st.session_state.hsk_level)
        mode = st.selectbox(
            "学习模式 Learning Mode",
            ["general", "grammar", "vocabulary", "conversation", "correction", "listening"]
        )
    
    # Main chat interface
    user_input = st.text_input("输入中文 (Enter Chinese):", "")
    
    if user_input:
        response = assistant.generate_response(
            user_input,
            {"mode": mode, "hsk_level": st.session_state.hsk_level}
        )
        
        if response:
            st.write("### 回答 Response")
            st.write(response['chinese'])
            st.write("### 拼音 Pinyin")
            st.write(response['pinyin'])
            
            if response['key_vocabulary']:
                st.write("### 重要词汇 Key Vocabulary")
                for word in response['key_vocabulary']:
                    st.write(f"- {word['word']} ({word['pinyin']}) - HSK {word['hsk_level']}")