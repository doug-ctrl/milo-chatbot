from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk
import os
import wikipedia

# Ensures the missing piece is always there
nltk.download('punkt_tab')

# Initialize the bot
# Initialize the bot with logic filters
chatbot = ChatBot(
    "Milo",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    tagger_profile='chatterbot.tagging.PosHypernymTagger',

#Add pre-processors to help Milo "remember" clean versions of text
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand that yet. I am still learning',
            'maximum_similarity_threshold': 0.70
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        },
        {
            'import_path': 'chatterbot.logic.TimeLogicAdapter'
        }
    ]
)

# Train the chatbot with conversations.txt file
trainer = ListTrainer(chatbot)

#Read and train from an entire folder
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

print("Milo is ready! Type 'quit' or 'exit' to stop.")

exit_conditions = (":q", "quit", "exit")
while True:
    query = input("You: ")
    if query.lower() in exit_conditions:
        break

    # Check if the user is asking to "search" or "who/what is"
    if "search" in query.lower() or "who is" in query.lower() or "what is" in query.lower():
        print("🪴 Milo: Let me look that up for you...")
        try:
            # Get a short 2-sentence summary from Wikipedia
            search_query = query.replace("search", "").replace("who is", "").replace("what is", "")
            result = wikipedia.summary(search_query, sentences=2)
            print(f"🪴 Milo: According to Wikipedia, {result}")
            continue  # Skip the rest of the loop and start over
        except Exception:
            print("🪴 Milo: I tried to look that up, but I couldn't find a clear answer.")
            continue

    # If it's not a search, use the normal chatbot logic
    try:
        response = chatbot.get_response(query)
        print(f"🪴 Milo: {response}")
    except Exception:
        print("🪴 Milo: I'm sorry, that sentence confused me a bit!")