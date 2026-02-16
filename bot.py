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

# --- NEW: User Name / First Run Logic ---
user_name_file = 'user_name.txt'
if not os.path.exists(user_name_file):
    print("🪴 Milo: Hello! I don't believe we've met. I am Milo.")
    print("🪴 Milo: What is your name? ")
    name = input("You: ").strip()
    if not name:
        name = "Friend"  # Fallback if they just hit enter
    with open(user_name_file, 'w') as f:
        f.write(name)
    user_name = name
else:
    with open(user_name_file, 'r') as f:
        user_name = f.read().strip()

# UI Variety personalized with the user's name
greetings = [
    f"Hello {user_name}! I'm Milo. How can I help you today?",
    f"Milo online. Ready for your questions, {user_name}!",
    f"Hi {user_name}! What are we working on today?"
]
thinking_phrases = [
    "Let me check my internal library...",
    "Searching the world's knowledge...",
    "Give me a second to look that up.",
    "Checking Wikipedia for you..."
]

print(f"🪴 Milo: {random.choice(greetings)}")
print("Milo is ready! Type 'quit' or 'exit' to stop.")

exit_conditions = (":q", "quit", "exit")

while True:
    query = input("You: ").strip()

    if not query:
        print("🪴 Milo: I'm here! Did you want to ask me something?")
        continue

    if query.lower() in exit_conditions:
        print(f"🪴 Milo: Goodbye, {user_name}! Have a great day.")
        break

    # Wikipedia Search Trigger with "Identity Filter"
    search_triggers = ["search", "who is", "what is"]
    if any(word in query.lower() for word in search_triggers) and "name" not in query.lower() and "milo" not in query.lower():
        print(f"🪴 Milo: {random.choice(thinking_phrases)}")
        try:
            search_query = query.lower().replace("search", "").replace("who is", "").replace("what is", "").strip()
            result = wikipedia.summary(search_query, sentences=2)
            print(f"🪴 Milo: According to Wikipedia, {result}")
            continue
        except Exception:
            print("🪴 Milo: I searched everywhere, but I couldn't find a definitive answer for that.")
            continue

    # Main Chatbot Logic
    try:
        response = chatbot.get_response(query)
        print(f"🪴 Milo: {response}")
    except Exception:
        print("🪴 Milo: I'm sorry, I got a little confused by that sentence!")