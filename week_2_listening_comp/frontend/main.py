import streamlit as st
import sys
import os
import json
import logging
from datetime import datetime
from pathlib import Path

# Add parent directory to sys.path for backend imports
sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.question_generator import QuestionGenerator
from backend.audio_generator import AudioGenerator

# Set up logging for debugging purposes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Page configuration
st.set_page_config(
    page_title="JLPT Listening Practice",
    page_icon="🎧",
    layout="wide"
)

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "backend" / "data"
QUESTIONS_FILE = DATA_DIR / "stored_questions.json"

def load_stored_questions():
    """Load previously stored questions from JSON file."""
    if QUESTIONS_FILE.exists():
        try:
            with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error reading stored questions: {e}")
            return {}
    return {}

def save_question(question, practice_type, topic, audio_file=None):
    """Save a generated question to JSON file with metadata."""
    stored_questions = load_stored_questions()
    question_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    question_data = {
        "question": question,
        "practice_type": practice_type,
        "topic": topic,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "audio_file": audio_file
    }
    stored_questions[question_id] = question_data
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stored_questions, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Error saving question: {e}")
    return question_id

def render_sidebar():
    """Render sidebar for accessing saved questions."""
    stored_questions = load_stored_questions()
    st.sidebar.header("Saved Questions")
    if stored_questions:
        for qid, qdata in stored_questions.items():
            button_label = f"{qdata['practice_type']} - {qdata['topic']}\n{qdata['created_at']}"
            if st.sidebar.button(button_label, key=qid):
                st.session_state.current_question = qdata['question']
                st.session_state.current_practice_type = qdata['practice_type']
                st.session_state.current_topic = qdata['topic']
                st.session_state.current_audio = qdata.get('audio_file')
                st.session_state.feedback = None
                st.experimental_rerun()
    else:
        st.sidebar.info("No saved questions yet. Generate some to see them here!")

def render_practice_area():
    """Render the main interactive practice area."""
    # Initialize session state
    if 'question_generator' not in st.session_state:
        st.session_state.question_generator = QuestionGenerator()
    if 'audio_generator' not in st.session_state:
        st.session_state.audio_generator = AudioGenerator()
    for key in ['current_question', 'feedback', 'current_practice_type', 'current_topic', 'current_audio']:
        if key not in st.session_state:
            st.session_state[key] = None

    # Sidebar: Saved Questions
    render_sidebar()

    # Practice type and topic selection
    practice_type = st.selectbox("Select Practice Type", ["Dialogue Practice", "Phrase Matching"])
    topics = {
        "Dialogue Practice": ["Daily Conversation", "Shopping", "Restaurant", "Travel", "School/Work"],
        "Phrase Matching": ["Announcements", "Instructions", "Weather Reports", "News Updates"]
    }
    topic = st.selectbox("Select Topic", topics[practice_type])

    # Button to generate a new question
    if st.button("Generate New Question"):
        section_num = 2 if practice_type == "Dialogue Practice" else 3
        try:
            new_question = st.session_state.question_generator.generate_similar_question(section_num, topic)
            st.session_state.current_question = new_question
            st.session_state.current_practice_type = practice_type
            st.session_state.current_topic = topic
            st.session_state.feedback = None
            st.session_state.current_audio = None
            save_question(new_question, practice_type, topic)
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error generating question: {e}")
            logging.error(f"Error in question generation: {e}")

    # If a question exists, display it along with answer options and audio generation
    if st.session_state.current_question:
        st.subheader("Practice Scenario")
        question = st.session_state.current_question

        if practice_type == "Dialogue Practice":
            st.markdown("**Introduction:**")
            st.write(question.get('Introduction', 'No introduction available.'))
            st.markdown("**Conversation:**")
            st.write(question.get('Conversation', 'No conversation available.'))
        else:
            st.markdown("**Situation:**")
            st.write(question.get('Situation', 'No situation available.'))

        st.markdown("**Question:**")
        st.write(question.get('Question', 'No question text available.'))

        col1, col2 = st.columns([2, 1])

        with col1:
            options = question.get('Options', [])
            if st.session_state.feedback:
                correct_index = st.session_state.feedback.get('correct_answer', 1) - 1
                selected_index = st.session_state.selected_answer - 1 if 'selected_answer' in st.session_state else -1

                st.markdown("**Your Answer:**")
                for idx, option in enumerate(options):
                    if idx == correct_index and idx == selected_index:
                        st.success(f"{idx+1}. {option} ✓ (Correct!)")
                    elif idx == correct_index:
                        st.success(f"{idx+1}. {option} ✓ (Correct answer)")
                    elif idx == selected_index:
                        st.error(f"{idx+1}. {option} ✗ (Your answer)")
                    else:
                        st.write(f"{idx+1}. {option}")

                st.markdown("**Explanation:**")
                explanation = st.session_state.feedback.get('explanation', 'No explanation available.')
                if st.session_state.feedback.get('correct', False):
                    st.success(explanation)
                else:
                    st.error(explanation)

                if st.button("Try Another Question"):
                    st.session_state.feedback = None
                    st.experimental_rerun()
            else:
                selected = st.radio(
                    "Choose your answer:",
                    options,
                    format_func=lambda opt: f"{options.index(opt) + 1}. {opt}"
                )
                if selected and st.button("Submit Answer"):
                    selected_index = options.index(selected) + 1
                    st.session_state.selected_answer = selected_index
                    try:
                        st.session_state.feedback = st.session_state.question_generator.get_feedback(question, selected_index)
                    except Exception as e:
                        st.error(f"Error processing answer: {e}")
                        logging.error(f"Feedback generation error: {e}")
                    st.experimental_rerun()

        with col2:
            st.subheader("Audio")
            if st.session_state.current_audio:
                st.audio(st.session_state.current_audio)
            elif question:
                if st.button("Generate Audio"):
                    with st.spinner("Generating audio..."):
                        try:
                            # Clean up any previous audio file if exists
                            current_audio = st.session_state.get('current_audio')
                            if current_audio and os.path.exists(current_audio):
                                try:
                                    os.remove(current_audio)
                                except Exception as remove_err:
                                    logging.warning(f"Error removing old audio: {remove_err}")
                            # Generate new audio and cache result
                            audio_file = st.session_state.audio_generator.generate_audio(question)
                            if not os.path.exists(audio_file):
                                raise FileNotFoundError("Audio file was not created")
                            st.session_state.current_audio = audio_file
                            # Update saved question with new audio file
                            save_question(question, practice_type, topic, audio_file)
                            st.experimental_rerun()
                        except Exception as e:
                            st.error(f"Error generating audio: {e}")
                            logging.error(f"Audio generation error: {e}")
            else:
                st.info("Generate a question first to enable audio.")

    else:
        st.info("Click 'Generate New Question' to start practicing!")

def main():
    st.title("JLPT Listening Practice")
    render_practice_area()

if __name__ == "__main__":
    main()
