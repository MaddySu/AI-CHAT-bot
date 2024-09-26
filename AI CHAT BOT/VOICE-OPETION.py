import pyttsx3

# Initialize the engine
engine = pyttsx3.init()

# Get all available voices
voices = engine.getProperty('voices')

# Print all available voices
for voice in voices:
    print("Voice:")
    print(" - ID: %s" % voice.id)
    print(" - Name: %s" % voice.name)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)
    print("\n")

# Select a voice (change the index to select a different voice)
selected_voice = voices[0]  # Change index as per your preference\\1 FOR MAIL 0 FOR FEMAIL
 

# Set the selected voice
engine.setProperty('voice', selected_voice.id)

# Test the selected voice
engine.say("Hello, I'm using a different voice.")
engine.runAndWait()
