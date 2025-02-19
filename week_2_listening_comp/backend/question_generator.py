import boto3
import json
from typing import Dict, List, Optional
from backend.vector_store import QuestionVectorStore
from pypinyin import pinyin, Style

class ChineseQuestionGenerator:
    def __init__(self):
        """Initialize Bedrock client and vector store"""
        self.bedrock_client = boto3.client('bedrock-runtime', region_name="us-east-1")
        self.vector_store = QuestionVectorStore()
        self.model_id = "amazon.titan-text-express-v1"  # Updated model for better Chinese support

    def _invoke_bedrock(self, prompt: str) -> Optional[str]:
        """Invoke Bedrock with the given prompt"""
        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "temperature": 0.7,
                        "topP": 0.9,
                        "maxTokens": 1000
                    }
                })
            )
            return json.loads(response['body'].read())['outputText']
        except Exception as e:
            print(f"调用 Bedrock 时出错: {str(e)}")  # Error invoking Bedrock
            return None

    def _generate_pinyin(self, text: str) -> str:
        """Generate Pinyin for Chinese text"""
        try:
            pinyin_list = pinyin(text, style=Style.TONE)
            return ' '.join([item[0] for item in pinyin_list])
        except Exception as e:
            return f"Error generating Pinyin: {str(e)}"

    def _process_chinese_text(self, text: Dict) -> Dict:
        """Add Pinyin and vocabulary analysis to Chinese text"""
        processed = {}
        for key, value in text.items():
            if isinstance(value, str):
                processed[key] = {
                    'text': value,
                    'pinyin': self._generate_pinyin(value)
                }
            elif isinstance(value, list):
                processed[key] = [
                    {'text': opt, 'pinyin': self._generate_pinyin(opt)}
                    for opt in value
                ]
        return processed

    def generate_similar_question(self, section_num: int, topic: str, hsk_level: int = 3) -> Dict:
        """Generate a new question similar to existing ones on a given topic"""
        similar_questions = self.vector_store.search_similar_questions(section_num, topic, n_results=3)
        
        if not similar_questions:
            return None
        
        # Create context from similar questions
        context = f"""以下是一些HSK {hsk_level}级听力题的例子：\n\n"""
        for idx, q in enumerate(similar_questions, 1):
            if section_num == 2:
                context += f"例子 {idx}:\n"
                context += f"介绍: {q.get('Introduction', '')}\n"
                context += f"对话: {q.get('Conversation', '')}\n"
                context += f"问题: {q.get('Question', '')}\n"
                if 'Options' in q:
                    context += "选项:\n"
                    for i, opt in enumerate(q['Options'], 1):
                        context += f"{i}. {opt}\n"
            else:  # section 3
                context += f"例子 {idx}:\n"
                context += f"情况: {q.get('Situation', '')}\n"
                context += f"问题: {q.get('Question', '')}\n"
                if 'Options' in q:
                    context += "选项:\n"
                    for i, opt in enumerate(q['Options'], 1):
                        context += f"{i}. {opt}\n"
            context += "\n"

        # Create prompt for generating new question
        prompt = f"""基于以下HSK {hsk_level}级听力题例子，创建一个关于{topic}的新题目。
        题目应该遵循相同的格式但与例子不同。
        确保题目测试听力理解能力，并有明确的正确答案。
        使用HSK {hsk_level}级的词汇和语法。
        
        {context}
        
        按照上述格式生成新题目。包括所有组成部分（介绍/情况、对话/问题和选项）。
        确保题目具有挑战性但公平，选项合理但只有一个明确的正确答案。
        仅返回题目，不要包含其他文本。
        
        新题目:
        """

        # Generate new question
        response = self._invoke_bedrock(prompt)
        if not response:
            return None

        # Parse the generated question
        try:
            lines = response.strip().split('\n')
            question = {}
            current_key = None
            current_value = []
            
            key_mapping = {
                "介绍:": "Introduction",
                "对话:": "Conversation",
                "情况:": "Situation",
                "问题:": "Question",
                "选项:": "Options"
            }
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                for cn_key, en_key in key_mapping.items():
                    if line.startswith(cn_key):
                        if current_key:
                            question[current_key] = ' '.join(current_value)
                        current_key = en_key
                        current_value = [line.replace(cn_key, "").strip()]
                        break
                elif line[0].isdigit() and line[1] == "." and current_key == 'Options':
                    current_value.append(line[2:].strip())
                elif current_key:
                    current_value.append(line)
            
            if current_key:
                if current_key == 'Options':
                    question[current_key] = current_value
                else:
                    question[current_key] = ' '.join(current_value)
            
            # Ensure we have exactly 4 options
            if 'Options' not in question or len(question.get('Options', [])) != 4:
                question['Options'] = [
                    "去图书馆学习",
                    "去咖啡店喝咖啡",
                    "去公园散步",
                    "去商店购物"
                ]
            
            # Add Pinyin and process Chinese text
            processed_question = self._process_chinese_text(question)
            
            # Add HSK level metadata
            processed_question['metadata'] = {
                'hsk_level': hsk_level,
                'topic': topic
            }
            
            return processed_question
            
        except Exception as e:
            print(f"解析生成的问题时出错: {str(e)}")  # Error parsing generated question
            return None

    def get_feedback(self, question: Dict, selected_answer: int) -> Dict:
        """Generate feedback for the selected answer"""
        if not question or 'Options' not in question:
            return None

        # Create prompt for generating feedback
        prompt = f"""根据以下HSK听力题和所选答案，提供解释说明是否正确以及原因。
        保持解释清晰简洁。
        
        """
        if 'Introduction' in question:
            prompt += f"介绍: {question['Introduction']['text']}\n"
            prompt += f"对话: {question['Conversation']['text']}\n"
        else:
            prompt += f"情况: {question['Situation']['text']}\n"
        
        prompt += f"问题: {question['Question']['text']}\n"
        prompt += "选项:\n"
        for i, opt in enumerate(question['Options'], 1):
            prompt += f"{i}. {opt['text']}\n"
        
        prompt += f"\n选择的答案: {selected_answer}\n"
        prompt += "\n请用JSON格式提供反馈，包含以下字段：\n"
        prompt += "- correct: true/false\n"
        prompt += "- explanation: 简短解释为什么答案正确/错误\n"
        prompt += "- explanation_pinyin: 解释的拼音\n"
        prompt += "- correct_answer: 正确选项的编号 (1-4)\n"

        # Get feedback
        response = self._invoke_bedrock(prompt)
        if not response:
            return None

        try:
            # Parse the JSON response
            feedback = json.loads(response.strip())
            # Add Pinyin for the explanation
            if 'explanation' in feedback:
                feedback['explanation_pinyin'] = self._generate_pinyin(feedback['explanation'])
            return feedback
        except:
            # If JSON parsing fails, return a basic response
            return {
                "correct": False,
                "explanation": "无法生成详细反馈，请重试。",
                "explanation_pinyin": "wú fǎ shēng chéng xiáng xì fǎn kuì, qǐng chóng shì.",
                "correct_answer": 1
            }