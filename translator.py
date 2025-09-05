# import speech_recognition as sr
# from translate import Translator
# from gtts import gTTS
# import os
# import sys
# import time # Added this import for the sleep function

# # Define a dictionary of supported languages and their codes.
# # This list is a curated intersection of languages supported by the
# # speech_recognition, translate, and gTTS libraries.
# LANGUAGES = {
#     'en': 'English',
#     'es': 'Spanish',
#     'fr': 'French',
#     'de': 'German',
#     'ja': 'Japanese',
#     'hi': 'Hindi',
#     'ru': 'Russian',
#     'it': 'Italian',
#     'pt': 'Portuguese',
#     'ko': 'Korean',
#     'zh': 'Chinese (Mandarin)',
#     'ar': 'Arabic',
#     # Add more languages here if you verify they are supported by all three libraries.
# }

# def get_language_choice(prompt_text):
#     """
#     Displays the supported languages and prompts the user for a choice.
#     Returns the selected language code.
#     """
#     print("------------------------------------------")
#     print(prompt_text)
#     print("------------------------------------------")
    
#     # Sort the languages alphabetically by name for a better user experience
#     sorted_languages = sorted(LANGUAGES.items(), key=lambda item: item[1])
    
#     for code, name in sorted_languages:
#         print(f"[{code}] {name}")
    
#     while True:
#         choice = input("Enter the language code from the list above: ").lower()
#         if choice in LANGUAGES:
#             return choice
#         else:
#             print("Invalid choice. Please enter a valid language code.")

# def main():
#     """
#     Main function to run the interactive speech translator.
#     """
#     try:
#         # Get user's desired input language
#         source_lang_code = get_language_choice("Please select the source language for your speech:")
#         source_lang_name = LANGUAGES[source_lang_code]
#         print(f"\nSource language selected: {source_lang_name}")

#         # Get user's desired output language
#         target_lang_code = get_language_choice("Please select the target language for the translation:")
#         target_lang_name = LANGUAGES[target_lang_code]
#         print(f"\nTarget language selected: {target_lang_name}\n")
        
#         # Step 1: Listen to the user's speech
#         recognizer = sr.Recognizer()
#         with sr.Microphone() as source:
#             print(f"Say something in {source_lang_name}...")
#             # Adjust for ambient noise to improve recognition accuracy
#             recognizer.adjust_for_ambient_noise(source)
            
#             # Configure listening parameters for better audio capture
#             recognizer.energy_threshold = 4000  # Adjust sensitivity (default: 300)
#             recognizer.dynamic_energy_threshold = True  # Automatically adjust based on ambient noise
#             recognizer.pause_threshold = 0.8  # Wait 0.8 seconds of silence before stopping (default: 0.8)
#             recognizer.phrase_threshold = 0.3  # Minimum audio length to consider as a phrase (default: 0.3)
#             recognizer.non_speaking_duration = 0.5 # Stop listening after 0.5 seconds of silence (default: 0.5)
            
#             print("Listening... (speak now)")
#             audio = recognizer.listen(source, timeout=10, phrase_time_limit=65)
#             print("Audio captured successfully!")

#         # Step 2: Convert speech to text
#         print("Recognizing...")
#         # Use the user-selected language code for speech recognition
#         text = recognizer.recognize_google(audio, language=source_lang_code)
#         print(f"You said: {text}")

#         # Step 3: Translate the text
#         # Use the user-selected language codes for translation
#         translator = Translator(from_lang=source_lang_code.split('-')[0], to_lang=target_lang_code.split('-')[0])
#         translated_text = translator.translate(text)
#         print(f"Translated text: {translated_text}")

#         # Step 4: Convert translated text to speech
#         # Use the user-selected language code for text-to-speech
#         tts = gTTS(text=translated_text, lang=target_lang_code)
#         tts.save("Tanslated_voice.mp3")
#         print("\nPlaying translated audio...")
#         # Play the audio file (this command works on Windows)
#         os.system("start Tanslated_voice.mp3")

#     except sr.UnknownValueError:
#         print("Could not understand audio.")
#     except sr.RequestError as e:
#         print(f"Could not request results from Google service; {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# if __name__ == "__main__":
#     main()


import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import os
import sys
import time
from datetime import datetime
import uuid

# Define a dictionary of supported languages and their codes.
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'ja': 'Japanese',
    'hi': 'Hindi',
    'ru': 'Russian',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ko': 'Korean',
    'zh': 'Chinese (Mandarin)',
    'ar': 'Arabic',
    'kn': 'Kannada',
    'tr': 'Turkish'
}

def save_translation_to_file(original_text, translated_text, source_lang, target_lang, audio_filename):
    """Saves a new translation record and audio filename to a local text file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"[{timestamp}] Type: Speech-to-Speech\n"
        f"Original Text: {original_text}\n"
        f"Translated Text: {translated_text}\n"
        f"Languages: {source_lang} -> {target_lang}\n"
        f"Audio File: {audio_filename}\n"
        "------------------------------------------\n"
    )
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
        # Create a unique filename for the audio file
        audio_filename = f"translated_{uuid.uuid4()}.mp3"
        audio_file_path = os.path.join("static", "audio", audio_filename)
        
        # Ensure the static/audio directory exists
        os.makedirs(os.path.dirname(audio_file_path), exist_ok=True)
        
        tts.save(audio_file_path)
        print(f"Audio file created: {audio_file_path}")
        
        # Play the audio file (optional, for local use)
        os.system(f"start {audio_file_path}")
        time.sleep(3)  # Give time for the audio to play
        
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

def main():
    """
    Main function to run the interactive speech translator.
    """
    try:
        source_lang_code = get_language_choice("Please select the source language for your speech:")
        source_lang_name = LANGUAGES[source_lang_code]
        print(f"\nSource language selected: {source_lang_name}")

        target_lang_code = get_language_choice("Please select the target language for the translation:")
        target_lang_name = LANGUAGES[target_lang_code]
        print(f"\nTarget language selected: {target_lang_name}\n")
        
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print(f"Say something in {source_lang_name}...")
            recognizer.adjust_for_ambient_noise(source)
            recognizer.energy_threshold = 4000
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 1.5
            recognizer.phrase_threshold = 0.3
            recognizer.non_speaking_duration = 2.0
            
            print("Listening... (speak now)")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=65)
            print("Audio captured successfully!")

        print("Recognizing...")
        text = recognizer.recognize_google(audio, language=source_lang_code)
        print(f"You said: {text}")

        translator = Translator(from_lang=source_lang_code.split('-')[0], to_lang=target_lang_code.split('-')[0])
        translated_text = translator.translate(text)
        print(f"Translated text: {translated_text}")

        audio_filename = text_to_speech_gtts(translated_text, target_lang_code)
        if audio_filename:
            save_translation_to_file(text, translated_text, source_lang_name, target_lang_name, audio_filename)

    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google service; {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()



# import speech_recognition as sr
# from translate import Translator
# from gtts import gTTS
# import os
# import sys
# import time
# from datetime import datetime

# # Define a dictionary of supported languages and their codes.
# LANGUAGES = {
#     'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
#     'ja': 'Japanese', 'hi': 'Hindi', 'ru': 'Russian', 'it': 'Italian',
#     'pt': 'Portuguese', 'ko': 'Korean', 'zh': 'Chinese (Mandarin)', 'ar': 'Arabic',
# }

# def save_translation_to_file(type, original_text, translated_text, source_lang, target_lang):
#     """Saves a new translation record to a local text file."""
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     entry = (
#         f"[{timestamp}] Type: {type}\n"
#         f"Original Text: {original_text}\n"
#         f"Translated Text: {translated_text}\n"
#         f"Languages: {source_lang} -> {target_lang}\n"
#         "------------------------------------------\n"
#     )
#     with open("history.txt", "a", encoding="utf-8") as f:
#         f.write(entry)
#     print("Translation history saved to history.txt.")

# def translate_and_speak(text, from_lang_code, from_lang_name, to_lang_code, to_lang_name):
#     """Translates text, speaks the result, and saves the history."""
#     try:
#         translator = Translator(from_lang=from_lang_code, to_lang=to_lang_code)
#         translated_text = translator.translate(text)
#         print(f"Translated text: {translated_text}")

#         tts = gTTS(text=translated_text, lang=to_lang_code)
#         audio_file = "translated_audio.mp3"
#         tts.save(audio_file)
        
#         os.system(f"start {audio_file}")
        
#         # Save to local file
#         save_translation_to_file("Speech-to-Speech", text, translated_text, from_lang_name, to_lang_name)
#     except Exception as e:
#         print(f"An error occurred: {e}")

# def get_language_choice(prompt_text):
#     """Displays the supported languages and prompts the user for a choice."""
#     print("------------------------------------------")
#     print(prompt_text)
#     print("------------------------------------------")
#     sorted_languages = sorted(LANGUAGES.items(), key=lambda item: item[1])
#     for code, name in sorted_languages:
#         print(f"[{code}] {name}")
#     while True:
#         choice = input("Enter the language code from the list above: ").lower()
#         if choice in LANGUAGES:
#             return choice, LANGUAGES[choice]
#         else:
#             print("Invalid choice. Please enter a valid language code.")

# def main():
#     """Main function to run the interactive speech translator."""
#     try:
#         source_lang_code, source_lang_name = get_language_choice("Please select the source language:")
#         target_lang_code, target_lang_name = get_language_choice("Please select the target language:")

#         print(f"\nTranslator is active. Speak now in {source_lang_name}...")
#         recognizer = sr.Recognizer()
#         with sr.Microphone() as source:
#             recognizer.adjust_for_ambient_noise(source)
#             audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
#         print("Recognizing...")
#         text = recognizer.recognize_google(audio, language=source_lang_code)
#         print(f"You said: {text}")

#         translate_and_speak(text, source_lang_code, source_lang_name, target_lang_code, target_lang_name)
#     except sr.UnknownValueError:
#         print("Could not understand audio.")
#     except sr.RequestError as e:
#         print(f"Could not request results from Google service; {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# if __name__ == "__main__":
#     main()





# import speech_recognition as sr
# from translate import Translator
# from gtts import gTTS
# import os
# import sys

# # Define a dictionary of supported languages and their codes.
# # This is a pre-compiled list based on common support across the libraries.
# # You can expand this list if a language is supported by all three APIs.
# # It is important to note that the translate library uses ISO 639-1 codes (e.g., 'en', 'es'),
# # while the speech_recognition and gTTS libraries may use BCP-47 tags (e.g., 'en-US', 'es-ES').
# # For simplicity and broad compatibility, we'll primarily use the two-letter ISO 639-1 codes.
# LANGUAGES = {
#     'en': 'English',
#     'es': 'Spanish',
#     'fr': 'French',
#     'de': 'German',
#     'ja': 'Japanese',
#     'zh-CN': 'Chinese (Simplified)',
#     'hi': 'Hindi',
#     'ru': 'Russian',
#     'pt': 'Portuguese',
#     'it': 'Italian',
#     'ko': 'Korean',
#     'ar': 'Arabic',
#     # Add more languages as needed, but verify they are supported by all three libraries.
# }

# def get_language_choice(prompt_text):
#     """
#     Displays the supported languages and prompts the user for a choice.
#     Returns the selected language code.
#     """
#     print("------------------------------------------")
#     print(prompt_text)
#     print("------------------------------------------")
    
#     # Sort the languages alphabetically by name for better user experience
#     sorted_languages = sorted(LANGUAGES.items(), key=lambda item: item[1])
    
#     for code, name in sorted_languages:
#         print(f"[{code}] {name}")
    
#     while True:
#         choice = input("Enter the language code from the list above: ").lower()
#         if choice in LANGUAGES:
#             return choice
#         else:
#             print("Invalid choice. Please enter a valid language code.")

# # Main program flow
# try:
#     # Get user's desired input language
#     source_lang_code = get_language_choice("Please select the source language for your speech:")
#     source_lang_name = LANGUAGES[source_lang_code]
#     print(f"\nSource language selected: {source_lang_name}\n")

#     # Get user's desired output language
#     target_lang_code = get_language_choice("Please select the target language for the translation:")
#     target_lang_name = LANGUAGES[target_lang_code]
#     print(f"\nTarget language selected: {target_lang_name}\n")
    
#     # Step 1: Listen to the user's speech
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print(f"Say something in {source_lang_name}...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)

#     # Step 2: Convert speech to text
#     print("Recognizing...")
#     text = recognizer.recognize_google(audio, language=source_lang_code)
#     print(f"You said: {text}")

#     # Step 3: Translate the text
#     translator = Translator(from_lang=source_lang_code, to_lang=target_lang_code)
#     translated_text = translator.translate(text)
#     print(f"Translated text: {translated_text}")

#     # Step 4: Convert translated text to speech
#     tts = gTTS(text=translated_text, lang=target_lang_code)
#     tts.save("Tanslated_voice.mp3")
#     print("\nPlaying translated audio...")
#     os.system("start Tanslated_voice.mp3")  # Plays the audio file on Windows

# except sr.UnknownValueError:
#     print(" Could not understand audio.")
# except sr.RequestError as e:
#     print(f" Could not request results from Google service; {e}")
# except Exception as e:
#     print(f" An error occurred: {e}")



# import speech_recognition as sr
# from translate import Translator
# from gtts import gTTS
# import os

# # Step 1: Listen to the user's speech
# recognizer = sr.Recognizer()
# with sr.Microphone() as source:
#     print("Say something...")
#     audio = recognizer.listen(source)

# # Step 2: Convert speech to text
# try:
#     text = recognizer.recognize_google(audio, language='en-US')  # Source language is English
#     print(f"You said: {text}")

#     # Step 3: Translate the text
#     translator = Translator(from_lang="en", to_lang="es")  # Translate from English to Spanish
#     translated_text = translator.translate(text)
#     print(f"Translated text: {translated_text}")

#     # Step 4: Convert translated text to speech
#     tts = gTTS(text=translated_text, lang='es')  # Target language is Spanish
#     tts.save("Tanslated_voice.mp3")
#     os.system("start Tanslated_voice.mp3") # Plays the audio file on Windows

# except sr.UnknownValueError:
#     print("Could not understand audio.")
# except sr.RequestError as e:
#     print(f"Could not request results; {e}")