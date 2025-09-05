# #two way commuication

import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import os
import sys
import time
from datetime import datetime
import uuid

LANGUAGES = {
    'en': 'English', 'hi': 'Hindi', 'kn': 'Kannada', 'es': 'Spanish',
    'fr': 'French', 'de': 'German', 'ja': 'Japanese', 'ru': 'Russian',
    'it': 'Italian', 'pt': 'Portuguese', 'ko': 'Korean', 'zh-CN': 'Chinese (Mandarin)',
    'ar': 'Arabic',
}

def saveing_translation(original_text, translated_text, source_lang, target_lang, audio_filename):
    """Saveing a new translation record and audio filename in the form of local text file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"[{timestamp}] Type: Two-Way Communication\n"
        f"Original Text: {original_text}\n"
        f"Translated Text: {translated_text}\n"
        f"Languages: {source_lang} -> {target_lang}\n"
        f"Audio File: {audio_filename}\n"
        "------------------------------------------\n"
    )
    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(entry)
    print("Translation history saved to history.txt.")

def translated_speech(text, from_lang, to_lang, from_lang_name, to_lang_name):
    """
    Translating the text to speech,which is the result, and save the audio file.
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

def language_selection(prompt_text):
    """Displaying the supported languages and prompts to the user for a choice."""
    print("------------------------------------------")
    print(prompt_text)
    print("------------------------------------------")
    sorted_lang = sorted(LANGUAGES.items(), key=lambda item: item[1])
    for code, name in sorted_lang:
        print(f"[{code}] {name}")
    while True:
        choice = input("Enter the language code from the list above: ").lower()
        if choice in LANGUAGES:
            return choice
        else:
            print("Invalid choice. Please enter a valid language code.")

def main():
    """Main function to run the two-way interactive speech translator."""
    try:
        source_lang_code = language_selection("Please select the source language for person 1:")
        target_lang_code = language_selection("Please select the target language for person 2:")
        
        source_lang_name = LANGUAGES[source_lang_code]
        target_lang_name = LANGUAGES[target_lang_code]
        
        print(f"\nConversation is set up for {source_lang_name} ↔ {target_lang_name}")
        print("Say 'exit' to end the conversation.")
        
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
                
                translated_text, audio_filename = translated_speech(spoken_text, source_lang_code, target_lang_code, source_lang_name, target_lang_name)
                if audio_filename:
                    saveing_translation(spoken_text, translated_text, source_lang_name, target_lang_name, audio_filename)
            
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

                if spoken_text.lower() == 'stop':
                    break
                
                translated_text, audio_filename = translated_speech(spoken_text, target_lang_code, source_lang_code, target_lang_name, source_lang_name)
                if audio_filename:
                    saveing_translation(spoken_text, translated_text, target_lang_name, source_lang_name, audio_filename)

            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google service; {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
