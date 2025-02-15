from flask import Flask, jsonify
from flask_cors import CORS
import logging

# Import all blueprints
from words import words_blueprint
from study_sessions import sessions_blueprint
from study_activities import activities_blueprint
from groups import groups_blueprint
from dashboard import dashboard_blueprint
from grammar import grammar_blueprint
from listening import listening_blueprint
from reading import reading_blueprint
from writing import writing_blueprint

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Register all blueprints with appropriate prefixes
app.register_blueprint(words_blueprint, url_prefix="/api/words")
app.register_blueprint(sessions_blueprint, url_prefix="/api/sessions")
app.register_blueprint(activities_blueprint, url_prefix="/api/activities")
app.register_blueprint(groups_blueprint, url_prefix="/api/groups")
app.register_blueprint(dashboard_blueprint, url_prefix="/api/dashboard")
app.register_blueprint(grammar_blueprint, url_prefix="/api/grammar")
app.register_blueprint(listening_blueprint, url_prefix="/api/listening")
app.register_blueprint(reading_blueprint, url_prefix="/api/reading")
app.register_blueprint(writing_blueprint, url_prefix="/api/writing")

@app.route("/")
def index():
    return jsonify({
        "message": "Welcome to the Extended Chinese Learning App! Explore vocabulary, sessions, grammar, listening, reading, writing, and more."
    })

# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error("Unhandled Exception: %s", e)
    return jsonify({"error": "Internal server error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
