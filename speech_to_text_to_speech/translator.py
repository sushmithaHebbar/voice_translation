import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import os
import sys
import time # Added this import for the sleep function

# Define a dictionary of supported languages and their codes.
# This list is a curated intersection of languages supported by the
# speech_recognition, translate, and gTTS libraries.
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
    # Add more languages here if you verify they are supported by all three libraries.
}

def get_language_choice(prompt_text):
    """
    Displays the supported languages and prompts the user for a choice.
    Returns the selected language code.
    """
    print("------------------------------------------")
    print(prompt_text)
    print("------------------------------------------")
    
    # Sort the languages alphabetically by name for a better user experience
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
        # Get user's desired input language
        source_lang_code = get_language_choice("Please select the source language for your speech:")
        source_lang_name = LANGUAGES[source_lang_code]
        print(f"\nSource language selected: {source_lang_name}")

        # Get user's desired output language
        target_lang_code = get_language_choice("Please select the target language for the translation:")
        target_lang_name = LANGUAGES[target_lang_code]
        print(f"\nTarget language selected: {target_lang_name}\n")
        
        # Step 1: Listen to the user's speech
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print(f"Say something in {source_lang_name}...")
            # Adjust for ambient noise to improve recognition accuracy
            recognizer.adjust_for_ambient_noise(source)
            
            # Configure listening parameters for better audio capture
            recognizer.energy_threshold = 4000  # Adjust sensitivity (default: 300)
            recognizer.dynamic_energy_threshold = True  # Automatically adjust based on ambient noise
            recognizer.pause_threshold = 0.8  # Wait 0.8 seconds of silence before stopping (default: 0.8)
            recognizer.phrase_threshold = 0.3  # Minimum audio length to consider as a phrase (default: 0.3)
            recognizer.non_speaking_duration = 0.5 # Stop listening after 0.5 seconds of silence (default: 0.5)
            
            print("Listening... (speak now)")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=65)
            print("Audio captured successfully!")

        # Step 2: Convert speech to text
        print("Recognizing...")
        # Use the user-selected language code for speech recognition
        text = recognizer.recognize_google(audio, language=source_lang_code)
        print(f"You said: {text}")

        # Step 3: Translate the text
        # Use the user-selected language codes for translation
        translator = Translator(from_lang=source_lang_code.split('-')[0], to_lang=target_lang_code.split('-')[0])
        translated_text = translator.translate(text)
        print(f"Translated text: {translated_text}")

        # Step 4: Convert translated text to speech
        # Use the user-selected language code for text-to-speech
        tts = gTTS(text=translated_text, lang=target_lang_code)
        tts.save("Tanslated_voice.mp3")
        print("\nPlaying translated audio...")
        # Play the audio file (this command works on Windows)
        os.system("start Tanslated_voice.mp3")

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