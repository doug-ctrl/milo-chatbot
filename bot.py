from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import nltk

#This line ensures the missing piece is always there
nltk.download('punkt_tab')

#Initialize the bot
chatbot = ChatBot(
            "Milo",
                  storage_adapter='chatterbot.storage.SQLStorageAdapter',
                  tagger_profile='chatterbot.tagging.PosHypernymTagger'
                )

#Create a trainer
#trainer = ChatterBotCorpusTrainer(chatbot)

#Train the bot based on the english corpus
#Teaches it greetings, conversations, and basic facts
#trainer.train("chatterbot.corpus.english")

print("Training Complete! You can now talk to the bot.")

exit_conditions = (":q","quit","exit")
while True:
    query = input(">")
    if query.lower() in exit_conditions:
        break
    else:
        print(f"🪴{chatbot.get_response(query)}")