"""
This script creates a GUI application that allows users to interact with a Google Generative AI model 
via text or voice commands. It integrates several functionalities including text-to-speech, speech recognition, 
web browsing, and a graphical user interface for a seamless user experience.

Modules:
    - google.generativeai as genai: For interacting with Google's Generative AI model.
    - pyttsx3: For text-to-speech functionality.
    - speech_recognition as sr: For converting speech to text.
    - webbrowser: For opening web pages.
    - tkinter: For creating the graphical user interface.
    - tkinter.scrolledtext: For a scrollable text widget in the GUI.

Functions:
    - speak(text): Uses pyttsx3 to convert text to speech.
    - takecommand(): Listens to the user's voice command and converts it to text using the speech_recognition module.
    - sendToAI(command): Sends the user's command to the Google Generative AI and handles the response.
    - append_text(text): Appends text to the chat window in the GUI.
    - on_enter(event): Handles the Enter key press event to send user input to the AI.
    - on_voice_command(): Handles the voice command button click to send voice input to the AI.

Usage:
    1. Run the script.
    2. Type your message in the text entry box and press Enter to send.
    3. Alternatively, click the "Voice Command" button and speak your message.
    4. The AI response will be displayed in the chat window and read aloud.
    5. Type "quit" or say "quit" to exit the application.

Note:
    - Ensure you have the necessary API key for Google Generative AI and the required packages installed.
    - The application currently supports basic commands such as "open YouTube" to demonstrate additional capabilities.

Exceptions:
    - Catches and handles exceptions for configuring Google Generative AI, generating AI responses, and recognizing speech.
"""

import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import webbrowser
import tkinter as tk
from tkinter import scrolledtext

# Configure Google Generative AI
try:
    genai.configure(api_key="AIzaSyDrNceK-ulqSX1q9XUFNPWioQg_-lMLwSo")
except Exception as e:
    print(f"Error configuring Google Generative AI: {e}")

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        append_text("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        append_text("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        append_text(f"You said: {query}")
        return query.lower()
    except Exception as e:
        append_text("Say that again...")
        return "None"

def sendToAI(command):
    try:
        response = genai.generate_text(prompt=command)
        ai_text = response.result
        append_text(f"AI: {ai_text}")
        
        speak(ai_text)
        
    except Exception as e:
        append_text(f"Error generating content: {e}")
        speak("Sorry, I couldn't generate a response.")

def append_text(text):
    chat_window.configure(state='normal')
    chat_window.insert(tk.END, text + '\n')
    chat_window.configure(state='disabled')
    chat_window.yview(tk.END)

def on_enter(event):
    user_input = user_entry.get()
    if user_input:
        append_text(f"You: {user_input}")
        user_entry.delete(0, tk.END)
        if user_input.lower() == "quit":
            root.destroy()
        elif "open youtube" in user_input.lower():
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        else:
            sendToAI(user_input)

def on_voice_command():
    voice_command = takecommand()
    if voice_command and voice_command != "None":
        append_text(f"You: {voice_command}")
        if voice_command.lower() == "quit":
            root.destroy()
        elif "open youtube" in voice_command.lower():
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        else:
            sendToAI(voice_command)

# Set up GUI
root = tk.Tk()
root.title("Chat with AI")
chat_frame = tk.Frame(root)
chat_frame.pack(pady=10)

chat_window = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=60, height=20, state='disabled')
chat_window.pack()

entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

user_entry = tk.Entry(entry_frame, width=50)
user_entry.pack(side=tk.LEFT, padx=10)
user_entry.bind("<Return>", on_enter)

voice_button = tk.Button(entry_frame, text="Voice Command", command=on_voice_command)
voice_button.pack(side=tk.RIGHT)

root.mainloop()
