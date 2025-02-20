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
    """Load prompts from YAML file"""
    with open('prompts.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# Setup logging
logger = logging.getLogger('japanese_app')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('gradio_app.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class JapaneseWritingApp:
    def __init__(self):
        self.client = OpenAI()
        self.vocabulary = None
        self.current_word = None
        self.current_sentence = None
        self.mocr = None
        self.load_vocabulary()

    def load_vocabulary(self):
        """Fetch vocabulary from API using group_id"""
        try:
            # Get group_id from environment variable or use default
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

    def generate_sentence(self, word):
        """Generate a sentence using OpenAI API"""
        logger.debug(f"Generating sentence for word: {word.get('kanji', '')}")
        
        try:
            prompts = load_prompts()
            messages = [
                {"role": "system", "content": prompts['sentence_generation']['system']},
                {"role": "user", "content": prompts['sentence_generation']['user'].format(word=word.get('kanji', ''))}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=100
            )
            sentence = response.choices[0].message.content.strip()
            logger.info(f"Generated sentence: {sentence}")
            return sentence
        except Exception as e:
            logger.error(f"Error generating sentence: {str(e)}")
            return "Error generating sentence. Please try again."

    def get_random_word_and_sentence(self):
        """Get a random word and generate a sentence"""
        logger.debug("Getting random word and generating sentence")
        
        if not self.vocabulary or not self.vocabulary.get('words'):
            return "No vocabulary loaded", "", "", "Please make sure vocabulary is loaded properly."
            
        self.current_word = random.choice(self.vocabulary['words'])
        self.current_sentence = self.generate_sentence(self.current_word)
        
        return (
            self.current_sentence,
            f"English: {self.current_word.get('english', '')}",
            f"Kanji: {self.current_word.get('kanji', '')}",
            f"Reading: {self.current_word.get('reading', '')}"
        )

    def grade_submission(self, image):
        """Process image submission and grade it using MangaOCR and LLM"""
        try:
            # Initialize MangaOCR for transcription if not already initialized
            if self.mocr is None:
                logger.info("Initializing MangaOCR")
                from manga_ocr import MangaOcr
                self.mocr = MangaOcr()
            
            # Transcribe the image
            logger.info("Transcribing image with MangaOCR")
            transcription = self.mocr(image)
            logger.debug(f"Transcription result: {transcription}")
            
            # Load prompts
            prompts = load_prompts()
            
            # Get literal translation
            logger.info("Getting literal translation")
            translation_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompts['translation']['system']},
                    {"role": "user", "content": prompts['translation']['user'].format(text=transcription)}
                ],
                temperature=0.3
            )
            translation = translation_response.choices[0].message.content.strip()
            logger.debug(f"Translation: {translation}")
            
            # Get grading and feedback
            logger.info("Getting grade and feedback")
            grading_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompts['grading']['system']},
                    {"role": "user", "content": prompts['grading']['user'].format(
                        target_sentence=self.current_sentence,
                        submission=transcription,
                        translation=translation
                    )}
                ],
                temperature=0.3
            )
            
            feedback = grading_response.choices[0].message.content.strip()
            # Parse grade and feedback from response
            grade = 'C'  # Default grade
            if 'Grade: S' in feedback:
                grade = 'S'
            elif 'Grade: A' in feedback:
                grade = 'A'
            elif 'Grade: B' in feedback:
                grade = 'B'
            
            # Extract just the feedback part
            feedback = feedback.split('Feedback:')[-1].strip()
            
            logger.info(f"Grading complete: {grade}")
            logger.debug(f"Feedback: {feedback}")
            
            return transcription, translation, grade, feedback
            
        except Exception as e:
            logger.error(f"Error in grade_submission: {str(e)}")
            return "Error processing submission", "Error processing submission", "C", f"An error occurred: {str(e)}"

def create_ui():
    app = JapaneseWritingApp()
    
    # Custom CSS for larger text
    custom_css = """
    .large-text-output textarea {
        font-size: 40px !important;
        line-height: 1.5 !important;
        font-family: 'Noto Sans JP', sans-serif !important;
    }
    """
    
    with gr.Blocks(
        title="Japanese Writing Practice",
        css=custom_css
    ) as interface:
        gr.Markdown("# Japanese Writing Practice")
        
        with gr.Row():
            with gr.Column():
                generate_btn = gr.Button("Generate New Sentence", variant="primary")
                # Make sentence output more prominent with larger text and more lines
                sentence_output = gr.Textbox(
                    label="Generated Sentence",
                    lines=3,
                    scale=2,  # Make the component larger
                    show_label=True,
                    container=True,
                    # Add custom CSS for larger text
                    elem_classes=["large-text-output"]
                )
                word_info = gr.Markdown("### Word Information")
                english_output = gr.Textbox(label="English", interactive=False)
                kanji_output = gr.Textbox(label="Kanji", interactive=False)
                reading_output = gr.Textbox(label="Reading", interactive=False)
            
            with gr.Column():
                image_input = gr.Image(label="Upload your handwritten sentence", type="filepath")
                submit_btn = gr.Button("Submit", variant="secondary")
                
                with gr.Group():
                    gr.Markdown("### Feedback")
                    transcription_output = gr.Textbox(
                        label="Transcription",
                        lines=3,
                        scale=2,
                        show_label=True,
                        container=True,
                        elem_classes=["large-text-output"]
                    )
                    translation_output = gr.Textbox(label="Translation", lines=2)
                    grade_output = gr.Textbox(label="Grade")
                    feedback_output = gr.Textbox(label="Feedback", lines=3)

        # Event handlers
        generate_btn.click(
            fn=app.get_random_word_and_sentence,
            outputs=[sentence_output, english_output, kanji_output, reading_output]
        )
        
        def handle_submission(image):
            return app.grade_submission(image)
            
        submit_btn.click(
            fn=handle_submission,
            inputs=[image_input],
            outputs=[transcription_output, translation_output, grade_output, feedback_output]
        )

    return interface

if __name__ == "__main__":
    interface = create_ui()
    interface.launch(server_name="0.0.0.0", server_port=8081)
import gradio as gr
import requests
import json
import random
import logging
from openai import OpenAI
import os
import dotenv
import yaml

# Load environment variables from .env file
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
# File handler for logging detailed debug information
fh = logging.FileHandler('gradio_app.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# ------------------------------------------------------------------------------
# ChineseWritingApp Class Definition
# ------------------------------------------------------------------------------
class ChineseWritingApp:
    """
    A class representing the core functionality of the Chinese Learning App.
    
    This class handles vocabulary loading, sentence generation via an LLM,
    and grading of user submissions through OCR and LLM-based evaluation.
    """
    
    def __init__(self):
        self.client = OpenAI()
        self.vocabulary = None
        self.current_word = None
        self.current_sentence = None
        self.mocr = None  # For MangaOCR or another OCR engine specialized for Chinese characters.
        self.load_vocabulary()

    def load_vocabulary(self):
        """
        Fetch vocabulary from an external API using a group_id.
        
        The API should return a JSON structure containing a list of words.
        If the API call fails, an empty vocabulary is assigned.
        """
        try:
            group_id = os.getenv('GROUP_ID', '1')
            url = f"http://localhost:5000/api/groups/{group_id}/words/raw"
            logger.debug(f"Fetching vocabulary from: {url}")
            
            response = requests.get(url)
            if response.status_code == 200:
                self.vocabulary = response.json()
                word_count = len(self.vocabulary.get('words', []))
                logger.info(f"Loaded {word_count} words from vocabulary.")
            else:
                logger.error(f"Failed to load vocabulary. HTTP status code: {response.status_code}")
                self.vocabulary = {"words": []}
        except Exception as e:
            logger.error(f"Exception while loading vocabulary: {str(e)}")
            self.vocabulary = {"words": []}

    def generate_sentence(self, word):
        """
        Generate a natural Chinese sentence using the OpenAI API based on a given word.
        
        Args:
            word (dict): A dictionary containing vocabulary details (e.g., 'character', 'pinyin', 'english').
        
        Returns:
            str: A generated sentence, or an error message if generation fails.
        """
        logger.debug(f"Generating sentence for word: {word.get('character', '')}")
        try:
            prompts = load_prompts()
            messages = [
                {"role": "system", "content": prompts['sentence_generation']['system']},
                {"role": "user", "content": prompts['sentence_generation']['user'].format(word=word.get('character', ''))}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=100
            )
            sentence = response.choices[0].message.content.strip()
            logger.info(f"Generated sentence: {sentence}")
            return sentence
        except Exception as e:
            logger.error(f"Error generating sentence: {str(e)}")
            return "Error generating sentence. Please try again."

    def get_random_word_and_sentence(self):
        """
        Select a random word from the loaded vocabulary and generate a corresponding sentence.
        
        Returns:
            tuple: A tuple containing the generated sentence and word details (English meaning, Chinese character, and reading/pinyin).
        """
        logger.debug("Selecting a random word and generating a sentence.")
        if not self.vocabulary or not self.vocabulary.get('words'):
            logger.error("No vocabulary available to select a word from.")
            return "No vocabulary loaded", "", "", "Please ensure vocabulary is loaded correctly."
            
        self.current_word = random.choice(self.vocabulary['words'])
        self.current_sentence = self.generate_sentence(self.current_word)
        
        return (
            self.current_sentence,
            f"English: {self.current_word.get('english', '')}",
            f"Character: {self.current_word.get('character', '')}",
            f"Pinyin: {self.current_word.get('pinyin', '')}"
        )

    def grade_submission(self, image):
        """
        Process a handwritten image submission by performing OCR and then grading the submission using AI.
        
        This function performs the following:
          - Initializes the OCR engine (if not already initialized).
          - Transcribes the image to extract Chinese text.
          - Translates the transcribed text to English.
          - Grades the submission based on the expected sentence, the transcription, and the literal translation.
        
        Args:
            image (str): The path to the uploaded image file.
        
        Returns:
            tuple: A tuple containing the transcription, translation, assigned grade, and detailed feedback.
        """
        try:
            # Initialize the OCR engine if necessary
            if self.mocr is None:
                logger.info("Initializing OCR engine for Chinese characters.")
                from manga_ocr import MangaOcr  # Ensure this package supports Chinese OCR
                self.mocr = MangaOcr()
            
            logger.info("Starting OCR transcription for the submitted image.")
            transcription = self.mocr(image)
            logger.debug(f"OCR transcription result: {transcription}")
            
            # Load prompts for translation and grading
            prompts = load_prompts()
            
            # Obtain a literal translation of the transcription using the OpenAI API
            logger.info("Requesting literal translation of the transcribed text.")
            translation_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompts['translation']['system']},
                    {"role": "user", "content": prompts['translation']['user'].format(text=transcription)}
                ],
                temperature=0.3
            )
            translation = translation_response.choices[0].message.content.strip()
            logger.debug(f"Obtained translation: {translation}")
            
            # Get grading and detailed feedback from the OpenAI API
            logger.info("Requesting grading and feedback for the submission.")
            grading_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompts['grading']['system']},
                    {"role": "user", "content": prompts['grading']['user'].format(
                        target_sentence=self.current_sentence,
                        submission=transcription,
                        translation=translation
                    )}
                ],
                temperature=0.3
            )
            grading_feedback = grading_response.choices[0].message.content.strip()
            
            # Determine grade from the feedback text
            grade = 'C'  # Default grade
            if 'Grade: S' in grading_feedback:
                grade = 'S'
            elif 'Grade: A' in grading_feedback:
                grade = 'A'
            elif 'Grade: B' in grading_feedback:
                grade = 'B'
            
            # Extract feedback text after "Feedback:" if available
            feedback = grading_feedback.split('Feedback:')[-1].strip()
            
            logger.info(f"Grading completed with grade {grade}.")
            logger.debug(f"Feedback: {feedback}")
            
            return transcription, translation, grade, feedback
            
        except Exception as e:
            logger.error(f"Error in grade_submission: {str(e)}")
            return "Error processing submission", "Error processing submission", "C", f"An error occurred: {str(e)}"

# ------------------------------------------------------------------------------
# Gradio User Interface Creation
# ------------------------------------------------------------------------------
def create_ui():
    """
    Build and return the Gradio Blocks interface for the Chinese Learning App.
    
    The interface provides tabs for:
      - Sentence Generation (showing generated sentence and word details)
      - Image submission and grading (for handwritten practice)
    """
    app = ChineseWritingApp()
    
    # Custom CSS styling for larger text outputs
    custom_css = """
    .large-text-output textarea {
        font-size: 40px !important;
        line-height: 1.5 !important;
        font-family: 'Noto Sans SC', sans-serif !important;
    }
    """
    
    with gr.Blocks(title="Chinese Writing Practice", css=custom_css) as interface:
        gr.Markdown("# Chinese Writing Practice")
        
        with gr.Row():
            with gr.Column():
                generate_btn = gr.Button("Generate New Sentence", variant="primary")
                sentence_output = gr.Textbox(
                    label="Generated Sentence",
                    lines=3,
                    scale=2,
                    show_label=True,
                    container=True,
                    elem_classes=["large-text-output"]
                )
                word_info = gr.Markdown("### Word Information")
                english_output = gr.Textbox(label="English", interactive=False)
                character_output = gr.Textbox(label="Character", interactive=False)
                pinyin_output = gr.Textbox(label="Pinyin", interactive=False)
            
            with gr.Column():
                image_input = gr.Image(label="Upload your handwritten sentence", type="filepath")
                submit_btn = gr.Button("Submit", variant="secondary")
                
                with gr.Group():
                    gr.Markdown("### Feedback")
                    transcription_output = gr.Textbox(
                        label="Transcription",
                        lines=3,
                        scale=2,
                        show_label=True,
                        container=True,
                        elem_classes=["large-text-output"]
                    )
                    translation_output = gr.Textbox(label="Translation", lines=2)
                    grade_output = gr.Textbox(label="Grade")
                    feedback_output = gr.Textbox(label="Feedback", lines=3)
        
        # Define event handlers for generating sentences and grading submissions
        generate_btn.click(
            fn=app.get_random_word_and_sentence,
            outputs=[sentence_output, english_output, character_output, pinyin_output]
        )
        
        def handle_submission(image):
            return app.grade_submission(image)
            
        submit_btn.click(
            fn=handle_submission,
            inputs=[image_input],
            outputs=[transcription_output, translation_output, grade_output, feedback_output]
        )

    return interface

# ------------------------------------------------------------------------------
# Main Application Entry Point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    interface = create_ui()
    interface.launch(server_name="0.0.0.0", server_port=8081)
