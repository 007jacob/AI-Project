from threading import current_thread
import openai
import speech_recognition as sr
from tkinter.constants import DISABLED, NORMAL
import tkinter as tk
from PIL import Image, ImageTk

# Set up OpenAI API credentials
openai.api_key = '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'

def ask_openai(question):
    model_engine = "text-davinci-003"
    prompt = f"Q: {question}\nA:"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = completions.choices[0].text.strip()
    return message

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand you."
    except sr.RequestError:
        return "Sorry, my speech recognition service is currently down."

class ChatbotGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("DonBOT")
        self.window.geometry("400x600")
        
  
        # Load the image and create a PhotoImage object
        image_path = "background_image.png"
        self.background_image = Image.open(image_path)
        self.bg_photo = ImageTk.PhotoImage(self.background_image)

        # Set the background image of the main window
        self.background_label = tk.Label(self.window, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.chat_frame = tk.Frame(self.window, bg="#BF0A30")
        self.chat_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.chat_history = tk.Text(self.chat_frame, wrap="word", state="disabled", bg="#BF0A30", fg="white", width=38, height=15)
        self.chat_history.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_history.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.chat_history.configure(yscrollcommand=self.scrollbar.set)

        self.question_entry = tk.Entry(self.window, width=30, font=("Times New Roman", 12), bg="white")
        self.question_entry.pack(pady=10)

        self.ask_button = tk.Button(self.window, text="Ask", width=30, command=self.ask_question, font=("Times New Roman", 12), bg="#000000", fg="black")
        self.ask_button.pack(pady=10)

        self.clear_button = tk.Button(self.window, text="Clear", width=30, command=self.clear_all, font=("Times New Roman", 12), bg="#000000", fg="black")
        self.clear_button.pack(pady=10)

        self.listen_button = tk.Button(self.window, text="Speak", width=30, command=self.listen_question, font=("Times New Roman", 12), bg="#000000", fg="black")
        self.listen_button.pack(pady=10)

        self.window.mainloop()

    def clear_all(self):
        self.chat_history.configure(state="normal")
        self.chat_history.delete("1.0", tk.END)
        self.chat_history.configure(state="disabled")

    def ask_question(self):
        question = self.question_entry.get().strip()
        if question != "":
            response = ask_openai(question)
            self.update_chat_history(question, response)

    def listen_question(self):
        question = recognize_speech()
        self.question_entry.delete(0, tk.END)
        self.question_entry.insert(0, question)
        response = ask_openai(question)
        self.update_chat_history(question, response)

    def update_chat_history(self, question, response):
        self.chat_history.configure(state="normal")

        # Get the current time and create the current_time variable   
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        if self.chat_history.index('end') != None:
            # Insert user's question with white text color and left alignment
            self.chat_history.insert('end', f"{current_time} You: {question}\n", 'user_message')
            self.chat_history.tag_configure('user_message', foreground='white', justify="left")
            
            # Insert AI's response with blue text color and right alignment
            self.chat_history.insert('end', f"{current_time} Don: {response}\n\n", 'ai_response')
            self.chat_history.tag_configure('ai_response', foreground='#5AAB61', justify="right")

        self.chat_history.configure(state="disabled")
        self.chat_history.yview('end')

if __name__ == "__main__":
    gui = ChatbotGUI() 