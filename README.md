# Milo AI Assistant 🪴

Milo is a modular, personality-driven chatbot built with Python and the ChatterBot library. He is designed to be a helpful companion that can handle conversations, perform mathematical calculations, and research information via Wikipedia.

## 🚀 Features
- **User Onboarding**: Milo greets new users and remembers their names for future sessions.
- **Modular Knowledge**: Training data is organized into specialized files (conversations, jokes, moods).
- **Global Research**: Integrated Wikipedia search for real-time information retrieval.
- **Math Logic**: Ability to solve mathematical equations on the fly.

## 🛠️ Installation
To run Milo locally, ensure you have Python installed and follow these steps:

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd chatbot
2. **Install dependencies**:
   ````bash
    pip install -r requirements.txt
3. **Run the bot**:
   ````bash
    python bot.py

## 📂 Project Structure
- **training_data/**: Contains .txt files used to train Milo's conversational brain.
- **bot.py**: The main application logic.
- **requirements.txt**: List of necessary Python libraries.
- **user_name.txt**: Stores the current user's name (ignored by Git).