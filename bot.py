from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk
import os

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
    else:
        try:
            response = chatbot.get_response(query)
            print(f"🪴 Milo: {response}")
        except Exception:
            # If the math logic or anything else breaks, Milo stays polite
            print("🪴 Milo: I'm sorry, that calculation or sentence confused me a bit!")