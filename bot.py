from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk
import os
import sys
import wikipedia
import random
import spacy

# --- HELPER FUNCTIONS FOR BUNDLING ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # If _MEIPASS doesn't exist, check if we are in a _onedir _internal folder
        base_path = os.path.join(os.path.dirname(sys.executable), "_internal")
        if not os.path.exists(base_path):
            base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_db_path():
    """ Ensures the database is created in a writable location """
    if getattr(sys, 'frozen', False):
        # If running as a bundled app, put DB in the same folder as the .app/exe
        return os.path.join(os.path.dirname(sys.executable), 'db.sqlite3')
    return 'db.sqlite3'

# --- INITIALIZATION ---
nltk.download('punkt_tab')

# 1. Define the model path using our resource helper
model_path = resource_path("en_core_web_sm")

# 2. Load the NLP model manually to pass into the bot
try:
    nlp_model = spacy.load(model_path)
except Exception as e:
    # Fallback for development mode if resource_path isn't needed
    nlp_model = spacy.load("en_core_web_sm")

chatbot = ChatBot(
    "Milo",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri=f'sqlite:///{get_db_path()}',
    # 3. FIX: Inject the loaded model directly into the tagger profile
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

# --- TRAINING LOGIC ---
trainer = ListTrainer(chatbot)
training_folder = resource_path('training_data')

if os.path.exists(training_folder):
    for filename in os.listdir(training_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(training_folder, filename), 'r', encoding='utf-8') as file:
                training_data = file.read().splitlines()
                trainer.train(training_data)
    print("Milo has learned everything from the training folder!")

# --- USER PERSISTENCE ---
if getattr(sys, 'frozen', False):
    user_name_file = os.path.join(os.path.dirname(sys.executable), 'user_name.txt')
else:
    user_name_file = 'user_name.txt'

def get_user_name():
    if not os.path.exists(user_name_file):
        return "Friend"
    with open(user_name_file, 'r') as f:
        return f.read().strip()

user_name = get_user_name()

# --- RESPONSE LOGIC ---
greetings = [
    f"Hello {user_name}! I'm Milo. How can I help you today?",
    f"Milo online. Ready for your questions, {user_name}!",
    f"Hi {user_name}! What are we working on today?"
]

def get_milo_response(query):
    query_lower = query.lower().strip()
    search_triggers = ["search", "who is", "what is", "tell me about", "who was", "what was"]
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
            return "I searched Wikipedia but couldn't find a page for that."
        except Exception:
            pass

    try:
        response = chatbot.get_response(query)
        return str(response)
    except Exception:
        return "I'm sorry, I got a little confused by that sentence!"

if __name__ == "__main__":
    pass