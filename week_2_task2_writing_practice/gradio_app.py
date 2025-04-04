import gradio as gr
import requests
import json
import random
import logging
from openai import OpenAI
import os
import dotenv
import yaml
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import time

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
        """Initialize the ChineseWritingApp with OpenAI client and caching."""
        self.client = OpenAI()
        self.vocabulary: Dict = {"words": []}
        self.current_word: Optional[Dict] = None
        self.current_sentence: Optional[str] = None
        self.mocr = None
        self.cache: Dict = {}
        self.last_refresh: float = 0
        self.refresh_interval: int = 3600  # 1 hour
        self.user_progress: Dict[str, List] = {
            "completed_words": [],
            "grades": [],
            "timestamps": []
        }
        self.load_vocabulary()

    def load_vocabulary(self) -> None:
        """
        Fetch vocabulary from an external API with caching and error handling.
        
        The API should return a JSON structure containing a list of words.
        Results are cached for the refresh_interval to prevent excessive API calls.
        """
        current_time = time.time()
        
        # Return cached vocabulary if it's still fresh
        if self.vocabulary["words"] and current_time - self.last_refresh < self.refresh_interval:
            logger.debug("Using cached vocabulary")
            return
            
        try:
            group_id = os.getenv('GROUP_ID', '1')
            url = f"http://localhost:5000/api/groups/{group_id}/words/raw"
            logger.debug(f"Fetching vocabulary from: {url}")
            
            response = requests.get(url, timeout=10)  # Add timeout
            response.raise_for_status()  # Raise exception for bad status codes
            
            self.vocabulary = response.json()
            self.last_refresh = current_time
            word_count = len(self.vocabulary.get('words', []))
            logger.info(f"Loaded {word_count} words from vocabulary.")
            
        except requests.Timeout:
            logger.error("Timeout while fetching vocabulary")
            if not self.vocabulary["words"]:  # Only set empty if we don't have cached data
                self.vocabulary = {"words": []}
                
        except requests.RequestException as e:
            logger.error(f"Request exception while loading vocabulary: {str(e)}")
            if not self.vocabulary["words"]:
                self.vocabulary = {"words": []}
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in vocabulary response: {str(e)}")
            if not self.vocabulary["words"]:
                self.vocabulary = {"words": []}
                
        except Exception as e:
            logger.error(f"Unexpected error while loading vocabulary: {str(e)}")
            if not self.vocabulary["words"]:
                self.vocabulary = {"words": []}

    def generate_sentence(self, word: Dict) -> str:
        """
        Generate a natural Chinese sentence using the OpenAI API with caching.
        
        Args:
            word (dict): A dictionary containing vocabulary details.
        
        Returns:
            str: A generated sentence, or an error message if generation fails.
        """
        logger.debug(f"Generating sentence for word: {word.get('character', '')}")
        
        # Check cache first
        cache_key = f"sentence_{word.get('character', '')}"
        if cache_key in self.cache:
            logger.debug("Using cached sentence")
            return self.cache[cache_key]
            
        try:
            prompts = load_prompts()
            if not prompts:
                raise ValueError("Failed to load prompt templates")
                
            messages = [
                {"role": "system", "content": prompts['sentence_generation']['system']},
                {"role": "user", "content": prompts['sentence_generation']['user'].format(
                    word=word.get('character', ''),
                    pinyin=word.get('pinyin', ''),
                    english=word.get('english', '')
                )}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=100
            )
            
            sentence = response.choices[0].message.content.strip()
            
            # Cache the result
            self.cache[cache_key] = sentence
            
            return sentence
            
        except Exception as e:
            error_msg = f"Error generating sentence: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def get_random_word_and_sentence(self) -> Tuple[str, str, str, str]:
        """
        Select a random word and generate a sentence, prioritizing unused words.
        
        Returns:
            tuple: (sentence, english, character, pinyin)
        """
        try:
            available_words = [
                word for word in self.vocabulary.get('words', [])
                if word.get('character') not in self.user_progress['completed_words']
            ]
            
            # If all words have been used, reset progress
            if not available_words:
                logger.info("All words completed, resetting progress")
                self.user_progress['completed_words'] = []
                available_words = self.vocabulary.get('words', [])
            
            if not available_words:
                raise ValueError("No vocabulary words available")
            
            self.current_word = random.choice(available_words)
            self.current_sentence = self.generate_sentence(self.current_word)
            
            return (
                self.current_sentence,
                self.current_word.get('english', ''),
                self.current_word.get('character', ''),
                self.current_word.get('pinyin', '')
            )
            
        except Exception as e:
            error_msg = f"Error getting word and sentence: {str(e)}"
            logger.error(error_msg)
            return (error_msg, '', '', '')

    def grade_submission(self, image: str) -> Tuple[str, str, str, str]:
        """
        Process and grade a handwritten submission with detailed feedback.
        
        Args:
            image (str): The path to the uploaded image file.
        
        Returns:
            tuple: (transcription, translation, grade, feedback)
        """
        if not self.current_word or not self.current_sentence:
            return (
                "No active exercise",
                "Please generate a new sentence first",
                "N/A",
                "Generate a new sentence before submitting"
            )
            
        try:
            # Initialize OCR if needed
            if not self.mocr:
                try:
                    from manga_ocr import MangaOcr
                    self.mocr = MangaOcr()
                except ImportError:
                    logger.error("Failed to initialize MangaOCR")
                    return (
                        "OCR Error",
                        "Failed to initialize OCR system",
                        "C",
                        "Please contact support for OCR setup"
                    )
            
            # Perform OCR
            transcription = self.mocr(image)
            logger.info(f"OCR Transcription: {transcription}")
            
            # Get translation and grading
            prompts = load_prompts()
            if not prompts:
                raise ValueError("Failed to load prompt templates")
            
            # Translation
            translation_messages = [
                {"role": "system", "content": prompts['translation']['system']},
                {"role": "user", "content": prompts['translation']['user'].format(text=transcription)}
            ]
            
            translation_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=translation_messages,
                temperature=0.3,
                max_tokens=100
            )
            translation = translation_response.choices[0].message.content.strip()
            
            # Grading
            grading_messages = [
                {"role": "system", "content": prompts['grading']['system']},
                {"role": "user", "content": prompts['grading']['user'].format(
                    target_word=self.current_word['character'],
                    target_sentence=self.current_sentence,
                    submission=transcription
                )}
            ]
            
            grading_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=grading_messages,
                temperature=0.3,
                max_tokens=200
            )
            grading_feedback = grading_response.choices[0].message.content.strip()
            
            # Parse grade and feedback
            grade = 'C'  # Default grade
            for possible_grade in ['S', 'A', 'B']:
                if f'Grade: {possible_grade}' in grading_feedback:
                    grade = possible_grade
                    break
            
            feedback = grading_feedback.split('Feedback:')[-1].strip()
            
            # Update progress
            if grade in ['S', 'A']:
                if self.current_word['character'] not in self.user_progress['completed_words']:
                    self.user_progress['completed_words'].append(self.current_word['character'])
                    self.user_progress['grades'].append(grade)
                    self.user_progress['timestamps'].append(datetime.now().isoformat())
            
            logger.info(f"Grading completed with grade {grade}")
            logger.debug(f"Feedback: {feedback}")
            
            return transcription, translation, grade, feedback
            
        except Exception as e:
            error_msg = f"Error in grade_submission: {str(e)}"
            logger.error(error_msg)
            return (
                "Error processing submission",
                "Error processing submission",
                "C",
                f"An error occurred: {str(e)}"
            )

# ------------------------------------------------------------------------------
# Gradio User Interface Creation
# ------------------------------------------------------------------------------
def create_ui():
    app = ChineseWritingApp()
    
    # Custom CSS styling for larger text outputs and modern UI
    custom_css = """
    .large-text-output textarea {
        font-size: 40px !important;
        line-height: 1.5 !important;
        font-family: 'Noto Sans SC', sans-serif !important;
    }
    
    .stats-container {
        padding: 1rem;
        background: #f8fafc;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 20px;
        background: #e2e8f0;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: #3b82f6;
        transition: width 0.3s ease;
    }
    """
    
    with gr.Blocks(title="Chinese Writing Practice", css=custom_css) as interface:
        gr.Markdown("# Chinese Writing Practice")
        
        # Progress Statistics
        with gr.Row() as stats_row:
            with gr.Column():
                progress_md = gr.Markdown("### Progress", elem_classes=["stats-container"])
                words_completed = gr.Number(label="Words Completed", value=0)
                average_grade = gr.Number(label="Average Grade (S=4, A=3, B=2, C=1)", value=0)
                streak = gr.Number(label="Current Streak", value=0)
        
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
                image_input = gr.Image(
                    label="Upload your handwritten sentence",
                    type="filepath",
                    height=300
                )
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
        
        def update_stats():
            """Update progress statistics."""
            completed = len(app.user_progress['completed_words'])
            
            # Calculate average grade
            grade_values = {'S': 4, 'A': 3, 'B': 2, 'C': 1}
            grades = app.user_progress['grades']
            avg = sum(grade_values.get(g, 1) for g in grades) / max(len(grades), 1)
            
            # Calculate streak
            streak = 0
            if app.user_progress['grades']:
                for grade in reversed(app.user_progress['grades']):
                    if grade in ['S', 'A']:
                        streak += 1
                    else:
                        break
            
            return completed, avg, streak
        
        # Event handlers
        def on_generate():
            """Handle generate button click with stats update."""
            result = app.get_random_word_and_sentence()
            stats = update_stats()
            return [*result, *stats]
        
        generate_btn.click(
            fn=on_generate,
            outputs=[
                sentence_output,
                english_output,
                character_output,
                pinyin_output,
                words_completed,
                average_grade,
                streak
            ]
        )
        
        def handle_submission(image):
            """Handle submission with stats update."""
            result = app.grade_submission(image)
            stats = update_stats()
            return [*result, *stats]
        
        submit_btn.click(
            fn=handle_submission,
            inputs=[image_input],
            outputs=[
                transcription_output,
                translation_output,
                grade_output,
                feedback_output,
                words_completed,
                average_grade,
                streak
            ]
        )
        
        # Initialize stats
        completed, avg, current_streak = update_stats()
        words_completed.value = completed
        average_grade.value = avg
        streak.value = current_streak

    return interface

# ------------------------------------------------------------------------------
# Main Application Entry Point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    interface = create_ui()
    interface.launch(server_name="0.0.0.0", server_port=8081)
