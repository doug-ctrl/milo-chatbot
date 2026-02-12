from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk

# Ensures the missing piece is always there
nltk.download('punkt_tab')

# Initialize the bot
chatbot = ChatBot(
    "Milo",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    tagger_profile='chatterbot.tagging.PosHypernymTagger'
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
        # Keep your cool🪴 emoji!
        print(f"🪴 Milo: {chatbot.get_response(query)}")