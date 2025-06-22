import requests
from bs4 import BeautifulSoup
from services.local_llm import generate_local_response
import pyttsx3
import speech_recognition as sr

# Speak output aloud
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Voice input handler
def listen(prompt="🎤 Speak now...") -> str:
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print(prompt)
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, I couldn't understand.")
        return ""
    except sr.RequestError as e:
        print(f"❌ API error: {e}")
        return ""

# Parse elements from webpage
def parse_webpage(url: str):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
        links = [a.get_text(strip=True) for a in soup.find_all("a") if a.get("href")]
        buttons = [btn.get_text(strip=True) for btn in soup.find_all(["button", "input"]) if btn.get("type") in ["submit", "button"]]
        inputs = [inp.get("name") or inp.get("id") for inp in soup.find_all("input") if inp.get("type") not in ["submit", "button"]]
        forms = [form.get("action") for form in soup.find_all("form")]

        return {
            "headings": headings,
            "links": links,
            "buttons": buttons,
            "inputs": inputs,
            "forms": forms
        }

    except Exception as e:
        return {"error": str(e)}

# Prompt builder for initial description
def build_prompt(elements):
    return f"""
You are a helpful assistant for blind users.

Headings: {elements['headings']}
Links: {elements['links']}
Buttons: {elements['buttons']}
Inputs: {elements['inputs']}
Forms: {elements['forms']}

Explain what this page contains in clear, friendly language.
Describe any actions the user can take, such as clicking links or filling out forms.
"""

# Prompt builder for follow-up Q&A
def build_conversation_prompt(elements, user_question: str):
    return f"""
You are an assistant that helps blind users understand web pages. The user has just visited a page with the following elements:

Headings: {elements['headings']}
Links: {elements['links']}
Buttons: {elements['buttons']}
Inputs: {elements['inputs']}
Forms: {elements['forms']}

Now the user asked: "{user_question}"

Please answer clearly and helpfully in plain English.
"""

# Follow-up Q&A mode
def run_qna_mode(parsed):
    while True:
        print("\n🎤 You can now ask a question about this webpage, or say 'no question' or 'stop' to continue.")
        speak("You can now ask a question about this webpage, or say no question or stop to continue.")

        user_q = listen()

        if not user_q:
            print("❌ I didn't catch that. Please try again.")
            speak("I didn't catch that. Please try again.")
            continue

        user_q = user_q.lower()

        if any(phrase in user_q for phrase in ["no question", "stop", "nothing", "i'm done", "that's all"]):
            print("\n🛑 Exiting Q&A mode.")
            speak("Okay, exiting question and answer mode.")
            return

        followup_prompt = build_conversation_prompt(parsed, user_q)
        answer = generate_local_response(followup_prompt)

        print(f"\n💬 Answer: {answer}\n")
        speak(answer)

# Yes/No loop
def ask_yes_no(prompt_text="Do you want to open another page? Say 'yes' or 'no'.") -> bool:
    for attempt in range(3):
        print(f"\n🎤 {prompt_text}")
        speak(prompt_text)
        response = listen().lower()

        if "yes" in response:
            return True
        elif "no" in response:
            return False
        else:
            print("❌ I didn't catch that. Let's try again.")
            speak("I didn't catch that. Please say yes or no.")
    return False

# Main CLI assistant
def main():
    print("\n🔵 BlindNav CLI - AI Assistant for Blind Web Navigation (Offline)\n")
    print("🎤 Speak the website you want to visit (e.g., 'example.com'):\n")
    spoken_url = listen()
    if not spoken_url:
        print("❌ No valid input received.")
        return

    if not spoken_url.startswith("http"):
        spoken_url = "https://" + spoken_url.replace(" ", "").lower()

    print(f"\n🌐 Using URL: {spoken_url}\n")
    print("🔎 Parsing page...\n")
    parsed = parse_webpage(spoken_url)

    if "error" in parsed:
        print(f"❌ Error parsing page: {parsed['error']}")
        speak("Sorry, I couldn't load the webpage.")
        return

    if not any(parsed.values()):
        print("⚠️ This page does not contain accessible content in static HTML (likely uses JavaScript).")
        speak("Sorry, I couldn't read anything meaningful from this page.")
        return

    prompt = build_prompt(parsed)

    print("🧠 Generating response using Mistral 7B (offline)...")
    description = generate_local_response(prompt)

    print("\n🗣️ Description:\n")
    print(description)
    speak(description)

    # 🧠 Follow-up Q&A
    run_qna_mode(parsed)

    # 🔄 Ask to continue
    if ask_yes_no():
        main()
    else:
        print("\n👋 Goodbye!")
        speak("Goodbye!")

if __name__ == "__main__":
    main()
