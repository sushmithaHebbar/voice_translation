import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import os
import sys
import time
from datetime import datetime
import uuid
from dotenv import load_dotenv
import requests

# Load environment variables for API key
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL_TEXT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

# Define a dictionary of supported languages and their codes.
LANGUAGES = {
    'en': 'English', 'hi': 'Hindi', 'kn': 'Kannada', 'es': 'Spanish',
    'fr': 'French', 'de': 'German', 'ja': 'Japanese', 'ru': 'Russian',
    'it': 'Italian', 'pt': 'Portuguese', 'ko': 'Korean', 'zh-CN': 'Chinese (Mandarin)',
    'ar': 'Arabic', 'tr': 'Turkish'
}

def save_to_history_file(record_type, original_text, translated_text, source_lang, target_lang, audio_filename=None):
    """Saves a new translation record and audio filename to a local text file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"[{timestamp}] Type: {record_type}\n"
        f"Original Text: {original_text}\n"
        f"Translated Text: {translated_text}\n"
        f"Languages: {source_lang} -> {target_lang}\n"
    )
    if audio_filename:
        entry += f"Audio File: {audio_filename}\n"
    entry += "------------------------------------------\n"

    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(entry)
    print("Translation history saved to history.txt.")

def text_to_speech_gtts(text, lang):
    """
    Converts text to speech, saves the audio file, and returns the filename.
    """
    print("Generating and playing audio...")
    try:
        tts = gTTS(text=text, lang=lang)
        audio_filename = f"translated_{uuid.uuid4()}.mp3"
        audio_file_path = os.path.join("static", "audio", audio_filename)
        
        os.makedirs(os.path.dirname(audio_file_path), exist_ok=True)
        
        tts.save(audio_file_path)
        print(f"Audio file created: {audio_file_path}")
        
        os.system(f"start {audio_file_path}")
        time.sleep(3)
        
        return audio_filename
    except Exception as e:
        print(f"Error during audio generation or playback: {e}")
        return None

def get_language_choice(prompt_text):
    """
    Displays the supported languages and prompts the user for a choice.
    Returns the selected language code.
    """
    print("------------------------------------------")
    print(prompt_text)
    print("------------------------------------------")
    
    sorted_languages = sorted(LANGUAGES.items(), key=lambda item: item[1])
    
    for code, name in sorted_languages:
        print(f"[{code}] {name}")
    
    while True:
        choice = input("Enter the language code from the list above: ").lower()
        if choice in LANGUAGES:
            return choice
        else:
            print("Invalid choice. Please enter a valid language code.")

def translate_text(text, source_lang_code, target_lang_code):
    """
    Translates text from a source language to a target language using the Gemini API.
    """
    print("\nTranslating...")
    prompt = f"Translate the following text from {source_lang_code} to {target_lang_code}: \"{text}\""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(API_URL_TEXT, json=payload)
        response.raise_for_status()
        result = response.json()
        translated_text = result['candidates'][0]['content']['parts'][0]['text']
        return translated_text
    except requests.exceptions.RequestException as e:
        return f"Error during translation: {e}"
    except (KeyError, IndexError) as e:
        return f"Unexpected API response format: {e}"

def translated_speech(text, from_lang, to_lang):
    """
    Translates the text to speech, which is the result, and saves the audio file.
    Returns the translated text and audio filename.
    """
    try:
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        translated_text = translator.translate(text)
        print(f"Translated text: {translated_text}")

        tts = gTTS(text=translated_text, lang=to_lang)
        audio_filename = f"translated_{uuid.uuid4()}.mp3"
        audio_fpath = os.path.join("static", "audio", audio_filename)

        os.makedirs(os.path.dirname(audio_fpath), exist_ok=True)
        tts.save(audio_fpath)
        
        os.system(f"start {audio_fpath}")
        time.sleep(3)
        
        return translated_text, audio_filename
    except Exception as e:
        print(f"An error occurred during translation or text-to-speech: {e}")
        return None, None

def run_text_translation():
    """Handles standard text translation."""
    input_text = input("Enter the text you want to translate: ")
    
    print("Available Languages:")
    for i, lang_code in enumerate(LANGUAGES):
        print(f"    {i+1}. {LANGUAGES[lang_code]} ({lang_code})")

    try:
        source_index = int(input("\nEnter the number for your source language: ")) - 1
        target_index = int(input("Enter the number for your target language: ")) - 1
        
        if not (0 <= source_index < len(LANGUAGES) and 0 <= target_index < len(LANGUAGES)):
            print("Invalid language numbers. Please choose from the list.")
            sys.exit(1)

        source_lang_code = list(LANGUAGES.keys())[source_index]
        target_lang_code = list(LANGUAGES.keys())[target_index]
        source_lang_name = LANGUAGES[source_lang_code]
        target_lang_name = LANGUAGES[target_lang_code]

    except ValueError:
        print("Invalid input. Please enter a number.")
        sys.exit(1)
    
    translated_text = translate_text(input_text, source_lang_code, target_lang_code)
    print("Translated Text:", translated_text)
    
    if not translated_text.startswith("Error"):
        audio_filename = text_to_speech_gtts(translated_text, target_lang_code)
        save_to_history_file("Text Translation", input_text, translated_text, source_lang_name, target_lang_name, audio_filename)

def run_two_way_communication():
    """Handles the two-way interactive speech translator."""
    try:
        source_lang_code = get_language_choice("Please select the source language for person 1:")
        target_lang_code = get_language_choice("Please select the target language for person 2:")
        
        source_lang_name = LANGUAGES[source_lang_code]
        target_lang_name = LANGUAGES[target_lang_code]
        
        print(f"\nConversation is set up for {source_lang_name} ↔ {target_lang_name}")
        print("Say 'stop' to end the conversation.")
        
        recognizer = sr.Recognizer()
        
        while True:
            # Direction 1: Listen to source language, translate to target
            with sr.Microphone() as source:
                print(f"\nPerson 1 ({source_lang_name}), say something...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
            
            try:
                spoken_text = recognizer.recognize_google(audio, language=source_lang_code)
                print(f"Person 1 said: {spoken_text}")
                
                if spoken_text.lower() == 'stop':
                    break
                
                translated_text, audio_filename = translated_speech(spoken_text, source_lang_code, target_lang_code)
                if audio_filename:
                    save_to_history_file("Two-Way Communication", spoken_text, translated_text, source_lang_name, target_lang_name, audio_filename)
            
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google service; {e}")

            # Direction 2: Listen to target language, translate to source
            with sr.Microphone() as source:
                print(f"\nPerson 2 ({target_lang_name}), say something...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
            
            try:
                spoken_text = recognizer.recognize_google(audio, language=target_lang_code)
                print(f"Person 2 said: {spoken_text}")

                if spoken_text.lower() == 'Stop':
                    break
                
                translated_text, audio_filename = translated_speech(spoken_text, target_lang_code, source_lang_code)
                if audio_filename:
                    save_to_history_file("Two-Way Communication", spoken_text, translated_text, target_lang_name, source_lang_name, audio_filename)

            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google service; {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """Main function to choose and run the appropriate translation mode."""
    print("------------------------------------------")
    print("Please select a translation mode:")
    print("1. Text Translation")
    print("2. Two-Way Communication")
    print("------------------------------------------")
    
    while True:
        choice = input("Enter your choice (1 or 2): ")
        if choice == '1':
            run_text_translation()
            break
        elif choice == '2':
            run_two_way_communication()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()