from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk

# Ensures the missing piece is always there
nltk.download('punkt_tab')

# Initialize the bot
# Initialize the bot with logic filters
chatbot = ChatBot(
    "Milo",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    tagger_profile='chatterbot.tagging.PosHypernymTagger',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand that yet. I am still learning',
            'maximum_similarity_threshold': 0.70
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        }
    ]
)

# Train the chatbot with conversations.txt file
trainer = ListTrainer(chatbot)

#Read and train from file
try:
    with open('conversations.txt', 'r') as file:
        training_data = file.read().splitlines()

    trainer.train(training_data)
    print("Milo has learned your custom conversations!")
except FileNotFoundError:
    print("Wait! I couldn't find conversations.txt. Make sure the file exists.")
# ------------------------------------------

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