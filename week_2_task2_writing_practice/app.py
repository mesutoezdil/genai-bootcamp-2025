import streamlit as st
import requests
from enum import Enum
import json
from typing import Optional, List, Dict
import openai
import logging
import random
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# ------------------------- Custom Logging Setup -------------------------
logger = logging.getLogger('chinese_learning_app')
logger.setLevel(logging.DEBUG)
if logger.hasHandlers():
    logger.handlers.clear()
file_handler = logging.FileHandler('chinese_app.log', mode='a')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - CHINESE_APP - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False

# ------------------------- Application State -------------------------
class AppState(Enum):
    SETUP = "setup"
    PRACTICE = "practice"
    REVIEW = "review"

# ------------------------- Main Application Class -------------------------
class ChineseLearningApp:
    def __init__(self):
        logger.debug("Initializing Chinese Learning App...")
        self.initialize_session_state()
        self.load_vocabulary()

    def initialize_session_state(self):
        """Initialize session state variables."""
        if 'app_state' not in st.session_state:
            st.session_state.app_state = AppState.SETUP
        if 'current_sentence' not in st.session_state:
            st.session_state.current_sentence = ""
        if 'review_data' not in st.session_state:
            st.session_state.review_data = None

    def load_vocabulary(self):
        """
        Load Chinese vocabulary from an external API using a provided group_id.
        The API returns a JSON with a list of words (each with 'character', 'pinyin', and 'english').
        """
        try:
            group_id = st.query_params.get('group_id', None)
            if not group_id:
                st.error("No group_id provided in query parameters.")
                self.vocabulary = None
                return

            api_url = f"http://localhost:5000/api/groups/{group_id}/words/raw"
            logger.debug(f"Fetching vocabulary from: {api_url}")
            response = requests.get(api_url)
            logger.debug(f"Vocabulary response status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    group_name = data.get('group_name', 'Unknown')
                    logger.debug(f"Received vocabulary for group: {group_name}")
                    self.vocabulary = data
                except Exception as e:
                    logger.error(f"JSON decode error: {e}")
                    st.error("Error decoding JSON from vocabulary API.")
                    self.vocabulary = None
            else:
                logger.error(f"API request failed with status: {response.status_code}")
                st.error(f"API request failed: {response.status_code}")
                self.vocabulary = None
        except Exception as e:
            logger.error(f"Failed to load vocabulary: {e}")
            st.error(f"Failed to load vocabulary: {str(e)}")
            self.vocabulary = None

    def generate_sentence(self, word: dict) -> str:
        """
        Generate a Chinese sentence using the OpenAI API based on the given word.
        The prompt instructs the AI to use simple grammar (HSK1-2 level) and to output both the Chinese sentence and its English translation.
        """
        character = word.get('character', '')
        prompt = f"""请使用汉字“{character}”生成一句简单、自然的中文句子，语法要求为HSK1-2水平。请仅返回以下格式的结果：
        
中文: [仅中文句子]
英文: [对应的英文翻译]
        """
        logger.debug(f"Generating sentence for word: {character}")
        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o",  # Replace with your available model identifier
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=100
            )
            result = response.choices[0].message.content.strip()
            logger.info(f"Generated sentence for '{character}': {result}")
            return result
        except Exception as e:
            logger.error(f"Error generating sentence for '{character}': {e}")
            return "Error generating sentence. Please try again."

    def grade_submission(self, image) -> Dict:
        """
        Process the submitted image and grade the handwritten Chinese sentence.
        (For demonstration purposes, this function returns mocked results.
         Replace with actual OCR integration and grading logic as needed.)
        """
        logger.debug("Starting grading process for the submitted image.")
        # TODO: Integrate OCR (e.g., using a Chinese-capable OCR engine) to transcribe the image.
        # For now, return mock grading data:
        mock_result = {
            "transcription": "今天我吃了面条",
            "translation": "I ate noodles today",
            "grade": "A",
            "feedback": "Well done! The sentence is grammatically correct, though minor improvements are possible."
        }
        logger.info("Grading complete with mock results.")
        return mock_result

    def render_setup_state(self):
        """Render the setup UI where users generate a new Chinese sentence."""
        logger.debug("Entering setup state UI.")
        st.title("Chinese Writing Practice")
        if not self.vocabulary:
            logger.debug("Vocabulary not loaded.")
            st.warning("Vocabulary not loaded. Please provide a valid group_id in the query parameters.")
            return

        # Button to generate a sentence
        generate_btn = st.button("Generate Sentence", key="gen_sentence_btn")
        logger.debug(f"Generate button clicked: {generate_btn}")

        if generate_btn:
            logger.info("Generate Sentence button clicked.")
            st.session_state['last_click'] = 'generate_sentence'
            if not self.vocabulary.get('words'):
                st.error("No words available in this vocabulary group.")
                return

            word = random.choice(self.vocabulary['words'])
            logger.debug(f"Selected word: {word.get('english')} - {word.get('character')}")
            sentence = self.generate_sentence(word)
            st.markdown("### Generated Sentence")
            st.write(sentence)
            st.session_state.current_sentence = sentence
            st.session_state.app_state = AppState.PRACTICE
            st.experimental_rerun()

    def render_practice_state(self):
        """Render the practice UI where users submit their handwritten sentence image."""
        st.title("Practice Your Chinese")
        st.write(f"Your Generated Sentence:\n{st.session_state.current_sentence}")
        uploaded_image = st.file_uploader("Upload an image of your handwritten sentence", type=['png', 'jpg', 'jpeg'])
        if st.button("Submit for Review") and uploaded_image:
            st.session_state.review_data = self.grade_submission(uploaded_image)
            st.session_state.app_state = AppState.REVIEW
            st.experimental_rerun()

    def render_review_state(self):
        """Render the review UI where users can see grading feedback."""
        st.title("Review Your Submission")
        st.write(f"Generated Sentence:\n{st.session_state.current_sentence}")
        review = st.session_state.review_data
        st.subheader("Grading Results")
        st.write(f"Transcription: {review['transcription']}")
        st.write(f"Translation: {review['translation']}")
        st.write(f"Grade: {review['grade']}")
        st.write(f"Feedback: {review['feedback']}")
        if st.button("Next Question"):
            st.session_state.app_state = AppState.SETUP
            st.session_state.current_sentence = ""
            st.session_state.review_data = None
            st.experimental_rerun()

    def run(self):
        """Determine the current app state and render the appropriate UI."""
        state = st.session_state.app_state
        logger.debug(f"Current app state: {state}")
        if state == AppState.SETUP:
            self.render_setup_state()
        elif state == AppState.PRACTICE:
            self.render_practice_state()
        elif state == AppState.REVIEW:
            self.render_review_state()

# ------------------------- Run the App -------------------------
if __name__ == "__main__":
    app = ChineseLearningApp()
    app.run()
