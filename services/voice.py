import pyttsx3
import speech_recognition as sr

def speak(text: str):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Error with the speech recognition service."
