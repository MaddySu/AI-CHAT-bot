import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime


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

speak("Hi, I am Robokidz. How can I help you?")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening...")
        r.pause_threshold = 2   
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        speak("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print(f"You said: {query}")
        return query.lower()
    except Exception as e:
        print("Say that again...")
        speak("Say that again...")
        return "None"

def sendToAI(command):
    try:
        response = genai.generate_text(prompt=command)
        ai_text = response.result
        speak(ai_text)
        print(ai_text)
    except Exception as e:
        print(f"Error generating content: {e}")
        speak("Sorry, I couldn't generate a response.")

def main():
    while True:
        text = takecommand()
        if text == "None":
            continue
        
        if "open youtube" in text:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif "time" in text:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")
        elif "date" in text:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today's date is {current_date}")
        elif "hi" in text:
            speak("Hi! How can I assist you?")
        elif "how are you" in text:
            speak("I'm doing great! Thanks for asking.")
            continue
        
        if "Bye" in text:
            speak("Goodbye!")
            break

        # Send the command to AI
        sendToAI(text)

if __name__ == "__main__":
    main()
