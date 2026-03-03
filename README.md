# Milo AI Assistant 🪴

Milo is a modular, personality-driven chatbot built with Python and the ChatterBot library. Recently upgraded with a professional GUI, Milo is designed to be a helpful blog companion that handles customer inquiries with a human-like touch.

## 🚀 Key Features
- **Professional GUI**: Built with `customtkinter` featuring Dark/Light mode persistence.
- **Support-First Onboarding**: Captures visitor names directly in the chat flow for a seamless experience.
- **Humanized Interaction**: Includes a 3-second "typing" delay to simulate thoughtful responses.
- **Readability Optimized**: Custom line spacing and message blocks for easy scanning of long technical answers.
- **Global Research & Math**: Integrated Wikipedia search and real-time equation solving.

## 🛠️ Installation
To run Milo locally, ensure you have Python installed and follow these steps:

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd chatbot
2. **Install dependencies**:
   ````bash
    pip install -r requirements.txt
3. **Run the application**:
   ````bash
    python gui.py

## 📂 Project Structure
- **gui.py**: The main Graphical User Interface logic
- **bot.py**: The core AI "brain" and logic processing.
- **training_data/**: Specialized .txt files (conversations, jokes, moods).
- **settings.json**: Stores UI preferences like Appearance Mode (ignored by Git)
- **milo.png**: The official application icon
- **requirements.txt**: List of necessary Python libraries.