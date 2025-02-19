import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.audio_generator import ChineseAudioGenerator
from pypinyin import pinyin, Style

# Test question data with Chinese content
test_question = {
    "Introduction": {
        "text": "请听下面的对话，然后回答问题。",
        "pinyin": "qǐng tīng xià miàn de duì huà, rán hòu huí dá wèn tí."
    },
    "Conversation": {
        "text": """
        男：请问，这趟地铁到北京站吗？
        女：是的，下一站就是北京站。
        男：谢谢。大概需要多长时间？
        女：让我想想，大约五分钟吧。
        """,
        "pinyin": """
        nán: qǐng wèn, zhè tàng dì tiě dào běi jīng zhàn ma?
        nǚ: shì de, xià yī zhàn jiù shì běi jīng zhàn.
        nán: xiè xie. dà gài xū yào duō cháng shí jiān?
        nǚ: ràng wǒ xiǎng xiǎng, dà yuē wǔ fēn zhōng ba.
        """
    },
    "Question": {
        "text": "到北京站需要多长时间？",
        "pinyin": "dào běi jīng zhàn xū yào duō cháng shí jiān?"
    },
    "Options": [
        {
            "text": "三分钟",
            "pinyin": "sān fēn zhōng"
        },
        {
            "text": "五分钟",
            "pinyin": "wǔ fēn zhōng"
        },
        {
            "text": "十分钟",
            "pinyin": "shí fēn zhōng"
        },
        {
            "text": "十五分钟",
            "pinyin": "shí wǔ fēn zhōng"
        }
    ],
    "metadata": {
        "hsk_level": 3,
        "topic": "交通",
        "correct_answer": 1  # 0-based index
    }
}

class ChineseAudioTester:
    def __init__(self):
        """Initialize the audio tester with Chinese support"""
        print("初始化音频生成器...")  # Initializing audio generator
        self.generator = ChineseAudioGenerator()

    def _generate_pinyin(self, text: str) -> str:
        """Generate Pinyin for Chinese text"""
        try:
            pinyin_list = pinyin(text, style=Style.TONE)
            return ' '.join([item[0] for item in pinyin_list])
        except Exception as e:
            return f"Error generating Pinyin: {str(e)}"

    def test_conversation_parsing(self, question: dict) -> None:
        """Test parsing of Chinese conversation"""
        print("\n解析对话内容...")  # Parsing conversation
        parts = self.generator.parse_conversation(question)
        
        print("\n解析后的对话部分:")  # Parsed conversation parts
        for speaker, text, gender in parts:
            print(f"说话者 (Speaker): {speaker} ({gender})")
            print(f"文本 (Text): {text}")
            print(f"拼音 (Pinyin): {self._generate_pinyin(text)}")
            print("---")

    def test_audio_generation(self, question: dict) -> str:
        """Test audio generation for Chinese content"""
        print("\n生成音频文件...")  # Generating audio file
        audio_file = self.generator.generate_audio(question)
        print(f"音频文件已生成: {audio_file}")  # Audio file generated
        return audio_file

    def validate_chinese_content(self, question: dict) -> None:
        """Validate Chinese content and Pinyin"""
        print("\n验证中文内容...")  # Validating Chinese content
        
        required_fields = ["Introduction", "Conversation", "Question", "Options"]
        for field in required_fields:
            if field not in question:
                raise ValueError(f"缺少必要字段: {field}")  # Missing required field
            
            if field == "Options":
                if not isinstance(question[field], list) or len(question[field]) != 4:
                    raise ValueError("选项必须包含4个选择")  # Options must contain 4 choices
                
                for option in question[field]:
                    if not isinstance(option, dict) or "text" not in option:
                        raise ValueError("选项格式错误")  # Invalid option format
            else:
                if not isinstance(question[field], dict) or "text" not in question[field]:
                    raise ValueError(f"{field} 格式错误")  # Invalid field format

    def run_tests(self, question: dict) -> None:
        """Run all tests for Chinese audio generation"""
        try:
            print("开始测试中文音频生成...")  # Starting Chinese audio generation test
            
            # Validate content
            self.validate_chinese_content(question)
            
            # Test conversation parsing
            self.test_conversation_parsing(question)
            
            # Test audio generation
            audio_file = self.test_audio_generation(question)
            
            print("\n测试成功完成！")  # Test completed successfully
            print(f"音频文件位置: {audio_file}")  # Audio file location
            
            # Print metadata
            if "metadata" in question:
                print("\n元数据:")  # Metadata
                print(f"HSK级别: {question['metadata'].get('hsk_level', 'Unknown')}")
                print(f"主题: {question['metadata'].get('topic', 'Unknown')}")
                print(f"正确答案: 选项 {question['metadata'].get('correct_answer', 'Unknown') + 1}")
                
        except Exception as e:
            print(f"\n测试过程中出错: {str(e)}")  # Error during test

if __name__ == "__main__":
    tester = ChineseAudioTester()
    tester.run_tests(test_question)