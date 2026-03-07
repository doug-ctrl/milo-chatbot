from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk
import os
import sys
import wikipedia
import random
import spacy
import requests  # Added for timeout handling


# --- HELPER FUNCTIONS FOR BUNDLING & DEPLOYMENT ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev, PyInstaller, and Cloud """
    try:
        base_path = sys._MEIPASS
    except Exception:
        internal_path = os.path.join(os.path.dirname(sys.executable), "_internal")
        if os.path.exists(internal_path):
            base_path = internal_path
        else:
            base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_db_path():
    """ Ensures the database is created in a writable location """
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), 'db.sqlite3')
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db.sqlite3')


# --- INITIALIZATION ---
nltk.download('punkt_tab')

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


# --- SMART TRAINING LOGIC ---
def train_milo():
    # syncs with the training_data folder on Render.
    print("Milo is checking for new training data...")
    trainer = ListTrainer(chatbot)
    training_folder = resource_path('training_data')

    if os.path.exists(training_folder):
        # process every .txt file found in the folder
        files = [f for f in os.listdir(training_folder) if f.endswith(".txt")]

        for filename in files:
            print(f"Milo is learning from: {filename}")
            with open(os.path.join(training_folder, filename), 'r', encoding='utf-8') as file:
                training_data = file.read().splitlines()
                if training_data:
                    trainer.train(training_data)

        print(f"Success! Milo has processed {len(files)} training files.")
    else:
        print("Warning: training_data folder not found!")


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


# --- IMPROVED RESPONSE LOGIC ---
def get_milo_response(query):
    query_lower = query.lower().strip()

    # 1. ALWAYS try ChatterBot first
    # This ensures your 'conversations.txt' answers win over Wikipedia
    try:
        response = chatbot.get_response(query)

        # If Milo is confident he found a match in your files, return it immediately
        if response.confidence > 0.75:
            return str(response)
    except Exception:
        pass

    # 2. Wikipedia Search (Only if ChatterBot isn't confident)
    search_triggers = ["search", "who is", "what is", "tell me about", "who was", "what was"]
    is_search = any(trigger in query_lower for trigger in search_triggers)
    is_identity = any(word in query_lower for word in ["your name", "milo", "who are you"])

    # Don't use Wikipedia for identity questions or if it's not a search trigger
    if is_search and not is_identity:
        try:
            search_term = query_lower
            for trigger in search_triggers:
                search_term = search_term.replace(trigger, "")
            search_term = search_term.replace("?", "").strip()

            # auto_suggest=False and a 5s timeout prevent the "Hanging"
            result = wikipedia.summary(search_term, sentences=1, auto_suggest=False)
            return f"According to Wikipedia, {result}"
        except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError, requests.exceptions.Timeout):
            pass

            # 3. Final Fallback to ChatterBot (even with low confidence)
    try:
        return str(chatbot.get_response(query))
    except Exception:
        return "I'm sorry, I got a little confused! Could you try that again?"


if __name__ == "__main__":
    print("Milo is ready. Type something!")