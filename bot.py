from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk
import os
import sys
import wikipedia
import random
import spacy


# --- HELPER FUNCTIONS FOR BUNDLING & DEPLOYMENT ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev, PyInstaller, and Cloud """
    try:
        base_path = sys._MEIPASS
    except Exception:
        # Check if _internal exists (PyInstaller onedir)
        internal_path = os.path.join(os.path.dirname(sys.executable), "_internal")
        if os.path.exists(internal_path):
            base_path = internal_path
        else:
            base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_db_path():
    """ Ensures the database is created in a writable location """
    # For Cloud deployment, we usually want the DB in the root project folder
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), 'db.sqlite3')
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db.sqlite3')


# --- INITIALIZATION ---
# Download NLTK data (Safe to run multiple times, checks for updates)
nltk.download('punkt_tab')

# Load the NLP model manually
model_path = resource_path("en_core_web_sm")
try:
    nlp_model = spacy.load(model_path)
except Exception:
    nlp_model = spacy.load("en_core_web_sm")

db_path = get_db_path()

chatbot = ChatBot(
    "Milo",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri=f'sqlite:///{db_path}',
    tagger_profile={
        'import_path': 'chatterbot.tagging.PosHypernymTagger',
        'language': nlp_model
    },
    preprocessors=['chatterbot.preprocessors.clean_whitespace'],
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand that yet. I am still learning!',
            'maximum_similarity_threshold': 0.70
        },
        {'import_path': 'chatterbot.logic.MathematicalEvaluation'}
    ]
)


# --- SMART TRAINING LOGIC (SKIP IF DB EXISTS) ---
def train_milo():
    # Only train if the database file doesn't exist yet
    # This prevents the web server from hanging during startup
    if not os.path.exists(db_path):
        print("First time setup: Training Milo...")
        trainer = ListTrainer(chatbot)
        training_folder = resource_path('training_data')

        if os.path.exists(training_folder):
            for filename in os.listdir(training_folder):
                if filename.endswith(".txt"):
                    with open(os.path.join(training_folder, filename), 'r', encoding='utf-8') as file:
                        training_data = file.read().splitlines()
                        trainer.train(training_data)
            print("Milo has learned everything!")
    else:
        print("Milo's brain is already loaded from database.")


# Execute the smart training
train_milo()

# --- USER PERSISTENCE ---
if getattr(sys, 'frozen', False):
    user_name_file = os.path.join(os.path.dirname(sys.executable), 'user_name.txt')
else:
    user_name_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'user_name.txt')


def get_user_name():
    if not os.path.exists(user_name_file):
        return "Friend"
    with open(user_name_file, 'r') as f:
        return f.read().strip()


user_name = get_user_name()


# --- RESPONSE LOGIC ---
def get_milo_response(query):
    query_lower = query.lower().strip()
    search_triggers = ["search", "who is", "what is", "tell me about", "who was", "what was"]

    # Check if this is a Wikipedia search
    is_search = any(trigger in query_lower for trigger in search_triggers)
    is_identity = any(word in query_lower for word in ["your name", "milo", "you"])
    is_math = any(char in query for char in "+-*/0123456789")

    if is_search and not is_identity and not is_math:
        try:
            search_term = query_lower
            for trigger in search_triggers:
                search_term = search_term.replace(trigger, "")
            search_term = search_term.replace("?", "").strip()
            search_results = wikipedia.search(search_term)
            if search_results:
                result = wikipedia.summary(search_results[0], sentences=2, auto_suggest=False)
                return f"According to Wikipedia, {result}"
        except Exception:
            pass

    try:
        response = chatbot.get_response(query)
        return str(response)
    except Exception:
        return "I'm sorry, I got a little confused by that sentence!"


if __name__ == "__main__":
    # Test block for local runs
    print("Milo is ready. Type something!")