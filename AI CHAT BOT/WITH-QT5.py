import sys
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import webbrowser
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QLineEdit, QPushButton, QLabel, QSizePolicy)

# Configure Google Generative AI
try:
    genai.configure(api_key="AIzaSyDrNceK-ulqSX1q9XUFNPWioQg_-lMLwSo")
except Exception as e:
    print(f"Error configuring Google Generative AI: {e}")

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chat with AI')
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)

        self.user_input = QLineEdit()
        self.user_input.returnPressed.connect(self.on_enter_pressed)

        self.voice_button = QPushButton('Voice Command')
        self.voice_button.clicked.connect(self.on_voice_command)

        vbox = QVBoxLayout()
        vbox.addWidget(self.chat_history)
        vbox.addWidget(self.user_input)

        hbox = QHBoxLayout()
        hbox.addWidget(self.voice_button)
        hbox.addStretch(1)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.speak("Hi, I am Robokidz. How can I help you?")

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.append_message("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            self.append_message("Recognizing...")
            query = r.recognize_google(audio, language="en-IN")
            self.append_message(f"You: {query}")
            return query.lower()
        except Exception as e:
            self.append_message("Say that again...")
            return "None"

    def send_to_ai(self, command):
        try:
            response = genai.generate_text(prompt=command)
            ai_text = response.result
            self.speak(ai_text)
            self.append_message(f"AI: {ai_text}")
        except Exception as e:
            self.append_message(f"Error generating content: {e}")
            self.speak("Sorry, I couldn't generate a response.")

    def append_message(self, text):
        current_text = self.chat_history.toPlainText()
        self.chat_history.setPlainText(current_text + '\n' + text)
        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())

    def on_enter_pressed(self):
        user_input = self.user_input.text()
        if user_input:
            self.append_message(f"You: {user_input}")
            self.user_input.clear()
            if user_input.lower() == "quit":
                self.close()
            elif "open youtube" in user_input.lower():
                self.speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")
            else:
                self.send_to_ai(user_input)

    def on_voice_command(self):
        voice_command = self.take_command()
        if voice_command and voice_command != "None":
            self.append_message(f"You: {voice_command}")
            if voice_command.lower() == "quit":
                self.close()
            elif "open youtube" in voice_command.lower():
                self.speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")
            else:
                self.send_to_ai(voice_command)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())
