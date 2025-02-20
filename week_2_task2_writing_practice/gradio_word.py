import gradio as gr
import requests
import json
import random
import logging
from openai import OpenAI
import os
import dotenv
import yaml

dotenv.load_dotenv()

def load_prompts():
    """
    Load prompt templates from a YAML configuration file.
    
    Returns:
        dict: A dictionary containing prompt configurations for:
              - Sentence Generation
              - Translation
              - Grading
    """
    try:
        with open('prompts.yaml', 'r', encoding='utf-8') as f:
            prompts = yaml.safe_load(f)
            return prompts
    except Exception as e:
        logger.error(f"Failed to load prompts.yaml: {str(e)}")
        return {}

# ------------------------------------------------------------------------------
# Logging Setup
# ------------------------------------------------------------------------------
logger = logging.getLogger('chinese_app')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('gradio_app.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class ChineseWritingApp:
    def __init__(self):
        self.client = OpenAI()
        self.vocabulary = None
        self.current_word = None
        self.current_sentence = None
        self.mocr = None
        # Get session_id from environment variable or default to '1'
        self.study_session_id = os.getenv('SESSION_ID', '1')
        logger.debug(f"Using session_id: {self.study_session_id}")
        self.load_vocabulary()

    def submit_result(self, is_correct):
        """Submit the grading result to the backend"""
        try:
            logger.debug(f"Attempting to submit result. Session ID: {self.study_session_id}, Word: {self.current_word}")
            
            if not self.study_session_id or not self.current_word:
                logger.error("Missing study session ID or current word")
                return

            url = f"http://localhost:5000/study_sessions/{self.study_session_id}/review"
            data = {
                'word_id': self.current_word.get('id'),
                'correct': is_correct
            }
            
            logger.debug(f"Submitting to URL: {url} with data: {data}")
            
            response = requests.post(url, json=data)
            logger.debug(f"Response status: {response.status_code}, content: {response.text}")
            
            if response.status_code == 200:
                logger.info(f"Successfully submitted result for word {self.current_word.get('id')}")
            else:
                logger.error(f"Failed to submit result. Status code: {response.status_code}")
        except Exception as e:
            logger.error(f"Error submitting result: {str(e)}")

    def load_vocabulary(self):
        """Fetch vocabulary from API using group_id"""
        try:
            group_id = os.getenv('GROUP_ID', '1')
            url = f"http://localhost:5000/api/groups/{group_id}/words/raw"
            logger.debug(f"Fetching vocabulary from: {url}")
            
            response = requests.get(url)
            if response.status_code == 200:
                self.vocabulary = response.json()
                logger.info(f"Loaded {len(self.vocabulary.get('words', []))} words")
            else:
                logger.error(f"Failed to load vocabulary. Status code: {response.status_code}")
                self.vocabulary = {"words": []}
        except Exception as e:
            logger.error(f"Error loading vocabulary: {str(e)}")
            self.vocabulary = {"words": []}

    def get_random_word(self):
        """Get a random word from vocabulary"""
        logger.debug("Getting random word")
        
        if not self.vocabulary or not self.vocabulary.get('words'):
            return "", "", "", "Please make sure vocabulary is loaded properly."
            
        self.current_word = random.choice(self.vocabulary['words'])
        
        return (
            f"Character: {self.current_word.get('character', '')}",
            f"Pinyin: {self.current_word.get('pinyin', '')}",
            f"English: {self.current_word.get('english', '')}",
            "Practice writing this word!"
        )

    def grade_submission(self, image):
        """Process image submission and grade it using MangaOCR and LLM"""
        try:
            # Initialize MangaOCR for transcription if not already initialized
            if self.mocr is None:
                logger.info("Initializing MangaOCR")
                from manga_ocr import MangaOcr
                self.mocr = MangaOcr()
            
            # Save the uploaded image to a temporary file
            import tempfile
            from PIL import Image
            import os
            img = Image.open(image)
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                img.save(temp_file.name)
                temp_path = temp_file.name
            
            logger.info("Transcribing image with MangaOCR")
            transcription = self.mocr(temp_path)
            logger.debug(f"Transcription result: {transcription}")
            
            os.unlink(temp_path)
            
            # Load prompts
            prompts = load_prompts()
            
            # Compare transcription with target word (assuming target is in 'character' field)
            is_correct = transcription.strip() == self.current_word.get('character', '').strip()
            result = "✓ Correct!" if is_correct else "✗ Incorrect"
            
            logger.debug(f"Current word: {self.current_word}")
            logger.debug(f"Transcription: {transcription}, Target: {self.current_word.get('character', '')}, Is correct: {is_correct}")
            
            # Submit result to backend
            self.submit_result(is_correct)
            
            logger.info(f"Grading complete: {result}")
            
            return transcription, result
            
        except Exception as e:
            logger.error(f"Error in grade_submission: {str(e)}")
            return "Error processing submission", "Error: " + str(e)

def create_ui():
    app = ChineseWritingApp()
    
    # Custom CSS for larger text outputs; update font for Chinese
    custom_css = """
    .large-text-output textarea {
        font-size: 40px !important;
        line-height: 1.5 !important;
        font-family: 'Noto Sans SC', sans-serif !important;
    }
    """
    
    with gr.Blocks(
        title="Chinese Word Writing Practice",
        css=custom_css
    ) as interface:
        gr.Markdown("# Chinese Word Writing Practice")
        
        with gr.Row():
            with gr.Column():
                generate_btn = gr.Button("Get New Word", variant="primary")
                character_output = gr.Textbox(
                    label="Character",
                    lines=2,
                    scale=2,
                    show_label=True,
                    container=True,
                    elem_classes=["large-text-output"],
                    interactive=False
                )
                pinyin_output = gr.Textbox(label="Pinyin", interactive=False)
                english_output = gr.Textbox(label="English", interactive=False)
                instruction_output = gr.Textbox(label="Instructions", interactive=False)
            
            with gr.Column():
                image_input = gr.Image(label="Upload your handwritten word", type="filepath")
                submit_btn = gr.Button("Submit", variant="secondary")
                
                with gr.Group():
                    gr.Markdown("### Results")
                    transcription_output = gr.Textbox(
                        label="Your Writing",
                        lines=1,
                        scale=2,
                        show_label=True,
                        container=True,
                        elem_classes=["large-text-output"]
                    )
                    grade_output = gr.Textbox(label="Result")
        
        # Event handlers
        generate_btn.click(
            fn=app.get_random_word,
            outputs=[character_output, pinyin_output, english_output, instruction_output]
        )
        
        submit_btn.click(
            fn=app.grade_submission,
            inputs=image_input,
            outputs=[transcription_output, grade_output]
        )
    return interface

if __name__ == "__main__":
    interface = create_ui()
    interface.launch(server_name="0.0.0.0", server_port=8081)
