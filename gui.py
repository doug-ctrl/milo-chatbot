import customtkinter as ctk
from bot import get_milo_response
from PIL import Image, ImageTk
import json
import os


class MiloGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Milo AI")
        self.geometry("400x650")

        try:
            icon_path = "milo.png"
            img = Image.open(icon_path)
            self.photo_icon = ImageTk.PhotoImage(img)
            self.wm_iconphoto(False, self.photo_icon)
        except Exception as e:
            print(f"Could not load icon: {e}")

        # --- UI ELEMENTS ---
        self.chat_display = ctk.CTkTextbox(self, width=380, height=450, state="disabled")
        self.chat_display.configure(spacing2=5)
        self.chat_display.pack(padx=10, pady=10)
        self.chat_display.tag_config("user", foreground="#3b8ed0")
        self.chat_display.tag_config("milo", foreground="#2fa572")

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=10, pady=5)

        self.user_input = ctk.CTkEntry(self.input_frame, width=380)
        self.user_input.pack(fill="x", pady=5)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=10, pady=5)

        self.send_button = ctk.CTkButton(self.button_frame, text="Send", width=180, command=self.send_message)
        self.send_button.pack(side="left", padx=(0, 5))

        self.clear_button = ctk.CTkButton(self.button_frame, text="Clear Chat", width=180,
                                          fg_color="transparent", border_width=1,
                                          command=self.clear_chat)
        self.clear_button.pack(side="right", padx=(5, 0))

        self.settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.settings_frame.pack(pady=(10, 20), fill="x", padx=10)

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.settings_frame, values=["System", "Dark", "Light"],
            command=self.change_appearance_mode_event, width=120)
        self.appearance_mode_optionemenu.pack(side="right", padx=10)

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12, "italic"), text_color="grey")
        self.status_label.pack(pady=(0, 5))

        # --- LOGIC STATE ---
        data = self.load_settings()
        ctk.set_appearance_mode(data["theme"])
        self.appearance_mode_optionemenu.set(data["theme"])

        self.user_name = None
        self.waiting_for_name = True

        self.bind("<Return>", lambda event: self.send_message())

        # First contact message
        self.update_chat("Milo: Welcome to Support! I am Milo. Before we begin, may I ask your name?", "milo")

    def send_message(self):
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.update_chat(f"You: {user_text}", "user")
        self.user_input.delete(0, 'end')
        self.user_input.focus()

        if self.waiting_for_name:
            self.user_name = user_text
            self.waiting_for_name = False
            # Transition with typing effect
            self.show_typing_and_respond(f"Thank you, {self.user_name}! How can I help you today?")
        else:
            self.status_label.configure(text="Milo is thinking...")
            self.update_idletasks()
            response = get_milo_response(user_text)
            self.status_label.configure(text="")
            # Response with typing effect
            self.show_typing_and_respond(response)

    def show_typing_and_respond(self, final_response):
        # 1. Show the "typing" indicator temporarily
        self.update_chat("Milo is typing...", "milo")

        # 2. Delay for 3 seconds to simulate a human-like response time
        self.after(3000, lambda: self.replace_typing_with_answer(final_response))

    def replace_typing_with_answer(self, final_response):
        # 3. Enable display to remove the "typing..." line
        self.chat_display.configure(state="normal")
        # end-3l deletes the typing line and its associated spacing
        self.chat_display.delete("end-4l", "end")
        self.chat_display.configure(state="disabled")

        # 4. Post the final answer
        self.update_chat(f"Milo: {final_response}", "milo")

    def load_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                return json.load(f)
        return {"theme": "System"}

    def save_settings(self):
        settings = {"theme": self.appearance_mode_optionemenu.get()}
        with open("settings.json", "w") as f:
            json.dump(settings, f)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        self.save_settings()

    def update_chat(self, message, tag):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", message + "\n\n\n", tag)
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def clear_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self.user_name = None
        self.waiting_for_name = True
        self.update_chat("Milo: Welcome to Support! I am Milo. Before we begin, may I ask your name?", "milo")


if __name__ == "__main__":
    app = MiloGUI()
    app.mainloop()