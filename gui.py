import customtkinter as ctk
from bot import get_milo_response
from PIL import Image, ImageTk

class MiloGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Milo AI")
        self.geometry("400x650") # Slightly taller to fit the new buttons

        try:
            icon_path = "milo.png"  # Make sure this matches your file name exactly
            img = Image.open(icon_path)

            # Use ImageTk to create a standard photo image for the title bar
            self.photo_icon = ImageTk.PhotoImage(img)
            self.wm_iconphoto(False, self.photo_icon)

            print("Icon loaded successfully!")
        except Exception as e:
            print(f"Could not load icon: {e}")

        # The Chat Display Area
        self.chat_display = ctk.CTkTextbox(self, width=380, height=450, state="disabled")
        self.chat_display.pack(padx=10, pady=10)

        # Tags for colors
        self.chat_display.tag_config("user", foreground="#3b8ed0")
        self.chat_display.tag_config("milo", foreground="#2fa572")

        # Input Frame Container
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=10, pady=5)

        # Parent is self.input_frame
        self.user_input = ctk.CTkEntry(self.input_frame, placeholder_text="Type a message...", width=380)
        self.user_input.pack(fill="x", pady=5)

        # Button Frame Container
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=10, pady=5)

        #Parent is self.button_frame
        self.send_button = ctk.CTkButton(self.button_frame, text="Send", width=180, command=self.send_message)
        self.send_button.pack(side="left", padx=(0, 5))

        # Clear Button
        self.clear_button = ctk.CTkButton(self.button_frame, text="Clear Chat", width=180,
                                          fg_color="transparent", border_width=1,
                                          command=self.clear_chat)
        self.clear_button.pack(side="right", padx=(5, 0))

        # Bind Enter key
        self.bind("<Return>", lambda event: self.send_message())

        # The Status Label
        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12, "italic"), text_color="grey")
        self.status_label.pack(pady=(0, 5))

    def send_message(self):
        user_text = self.user_input.get()
        if user_text:
            self.update_chat(f"You: {user_text}", "user")
            self.user_input.delete(0, 'end')

            # Show status
            self.status_label.configure(text="Milo is thinking...")
            self.update_idletasks()  # Forces the GUI to show the text NOW

            response = get_milo_response(user_text)

            # Hide status and show response
            self.status_label.configure(text="")
            self.update_chat(f"Milo: {response}", "milo")

    def update_chat(self, message, tag):
        self.chat_display.configure(state="normal")
        # Apply the color tag to the text being inserted
        self.chat_display.insert("end", message + "\n\n", tag)
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def clear_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")  # Deletes from line 1 to the end
        self.chat_display.configure(state="disabled")


if __name__ == "__main__":
    app = MiloGUI()
    app.mainloop()