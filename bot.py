from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk
import os
import wikipedia
import random

# Ensures the missing piece is always there
nltk.download('punkt_tab')

# Initialize the bot
chatbot = ChatBot(
    "Milo",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    tagger_profile='chatterbot.tagging.PosHypernymTagger',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand that yet. I am still learning!',
            'maximum_similarity_threshold': 0.70
        },
        {'import_path': 'chatterbot.logic.MathematicalEvaluation'}
    ]
)

# Training Logic
trainer = ListTrainer(chatbot)
training_folder = 'training_data'

if os.path.exists(training_folder):
    for filename in os.listdir(training_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(training_folder, filename), 'r') as file:
                training_data = file.read().splitlines()
                trainer.train(training_data)
    print("Milo has learned everything from the training folder!")
else:
    print(f"Wait! I couldn't find the {training_folder} folder.")

user_name_file = 'user_name.txt'


def get_user_name():
    if not os.path.exists(user_name_file):
        print("🪴 Milo: Hello! I don't believe we've met. I am Milo.")
        print("🪴 Milo: What is your name? ")
        name = input("You: ").strip()
        if not name:
            name = "Friend"
        with open(user_name_file, 'w') as f:
            f.write(name)
        return name
    else:
        with open(user_name_file, 'r') as f:
            return f.read().strip()


# Initialize variable for name
user_name = get_user_name() if os.path.exists(user_name_file) else "Friend"

# UI Variety personalized with the user's name
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
            #CLEANING: Strip the triggers
            search_term = query_lower
            for trigger in search_triggers:
                search_term = search_term.replace(trigger, "")
            search_term = search_term.replace("?", "").strip()

            # We search for the term first to get the official page title
            search_results = wikipedia.search(search_term)

            if search_results:
                # We take the top result and get its summary
                # auto_suggest=False prevents it from changing "Elon Musk" to something else
                result = wikipedia.summary(search_results[0], sentences=2, auto_suggest=False)
                return f"According to Wikipedia, {result}"
            else:
                return "I searched Wikipedia but couldn't find a page for that."

        except wikipedia.DisambiguationError as e:
            # If there are multiple Elons, pick the first one (usually the person)
            result = wikipedia.summary(e.options[0], sentences=2)
            return f"According to Wikipedia, {result}"
        except Exception:
            # If internet search fails completely, let ChatterBot try
            pass

    # 3. Fallback to normal chatbot logic
    try:
        response = chatbot.get_response(query)
        return str(response)
    except Exception:
        return "I'm sorry, I got a little confused by that sentence!"

# This block only runs if you run bot.py directly (Terminal Mode)
if __name__ == "__main__":
    user_name = get_user_name()
    print(f"🪴 Milo: {random.choice(greetings)}")
    print("Milo is ready! Type 'quit' or 'exit' to stop.")

    exit_conditions = (":q", "quit", "exit")

    while True:
        query = input("You: ").strip()
        if not query:
            continue
        if query.lower() in exit_conditions:
            print(f"🪴 Milo: Goodbye, {user_name}! Have a great day.")
            break

        # Use the central response function
        print(f"🪴 Milo: {get_milo_response(query)}")