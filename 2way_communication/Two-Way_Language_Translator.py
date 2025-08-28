import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import os
import sys
import time

# Define a dictionary of supported languages and their codes.
LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'kn': 'Kannada',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'ja': 'Japanese',
    'ru': 'Russian',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ko': 'Korean',
    'zh-CN': 'Chinese (Mandarin)',
    'ar': 'Arabic',
}

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

def translate_and_speak(text, from_lang, to_lang):
    """
    Translates text from one language to another and speaks the result.
    """
    try:
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        translated_text = translator.translate(text)
        print(f"Translated text: {translated_text}")

        tts = gTTS(text=translated_text, lang=to_lang)
        tts.save("translated_audio.mp3")
        os.system("start translated_audio.mp3")
    except Exception as e:
        print(f"An error occurred during translation or text-to-speech: {e}")

def main():
    """
    Main function to run the two-way interactive speech translator.
    """
    try:
        source_lang_code = get_language_choice("Please select the source language for person 1:")
        target_lang_code = get_language_choice("Please select the target language for person 2:")
        
        source_lang_name = LANGUAGES[source_lang_code]
        target_lang_name = LANGUAGES[target_lang_code]
        
        print(f"\nConversation is set up for {source_lang_name} ↔️ {target_lang_name}")
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
                
                if spoken_text.lower() == 'exit':
                    break
                
                translate_and_speak(spoken_text, source_lang_code, target_lang_code)
            
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

                if spoken_text.lower() == 'exit':
                    break
                
                translate_and_speak(spoken_text, target_lang_code, source_lang_code)

            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google service; {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
