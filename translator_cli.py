import os
import sys
import requests
from gtts import gTTS
from dotenv import load_dotenv 
from datetime import datetime
import time
import uuid

# Load environment variables from a .env file.
load_dotenv()

# Get your API key from environment variables.
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found. Please set it as an environment variable or in a .env file.")
API_URL_TEXT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

# List of supported languages.
SUPPORTED_LANGUAGES = {
    "en": "English",
    "kn": "Kannada",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "zh-CN": "Chinese (Simplified)",
    "ru": "Russian",
    "it": "Italian",
    "pt": "Portuguese",
    "ko": "Korean",
    "ar": "Arabic",
    "hi": "Hindi",
    "tr": "Turkish",
}

def save_to_history_file(record_type, original_text, translated_text, source_lang, target_lang, audio_filename=None):
    """Saves a new translation or announcement record to a local history.txt file."""
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
    print("Record saved to history.txt.")

def text_to_speech_gtts(text, lang):
    """
    Converts text to speech, saves the audio file in the static/audio directory, and plays it.
    Returns the filename.
    """
    print("Generating and playing audio...")
    try:
        tts = gTTS(text=text, lang=lang)
        
        # Ensure the static/audio directory exists
        audio_dir = os.path.join("static", "audio")
        os.makedirs(audio_dir, exist_ok=True)

        audio_filename = f"translated_{uuid.uuid4()}.mp3"
        audio_file_path = os.path.join(audio_dir, audio_filename)
        
        tts.save(audio_file_path)
        
        # This will play the audio file on most systems.
        os.system(f"start {audio_file_path}")
        print(f"Audio file created and played: {audio_file_path}")
        
        return audio_filename
    except Exception as e:
        print(f"Error during audio generation or playback: {e}")
        return None

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

def announce_identity(person_name, lang):
    """
    Synthesizes and plays a voice message announcing a person's identity.
    It also saves a record of the announcement to the history file.
    The language is now determined by the user's input.
    """
    print(f"Announcing identity: {person_name} in {SUPPORTED_LANGUAGES[lang]}.")
    text_to_announce = f"This is {person_name}."
    
    # Generate and play the audio.
    audio_filename = text_to_speech_gtts(text_to_announce, lang)
    
    # Save the announcement to the history file.
    save_to_history_file("Identity Announcement", person_name, text_to_announce, lang, lang, audio_filename)

def main():
    """Main function to handle command-line arguments and run the program."""
    if len(sys.argv) < 2:
        print("Usage: python translator_cli.py \"<text_to_translate>\"")
        print("Or: python translator_cli.py --announce \"<person_name>\"")
        sys.exit(1)

    # Check for the identity announcement flag.
    if sys.argv[1] == "--announce":
        if len(sys.argv) < 3:
            print("Please provide a name to announce.")
            sys.exit(1)
        
        person_name = sys.argv[2]
        
        # Prompt the user to select a language for the announcement.
        print("\nAvailable Languages for Announcement:")
        for i, lang_code in enumerate(SUPPORTED_LANGUAGES):
            print(f"    {i+1}. {SUPPORTED_LANGUAGES[lang_code]} ({lang_code})")
            
        try:
            target_index = int(input("\nEnter the number for your target language: ")) - 1
            if not (0 <= target_index < len(SUPPORTED_LANGUAGES)):
                print("Invalid language number. Please choose from the list.")
                sys.exit(1)
            target_lang_code = list(SUPPORTED_LANGUAGES.keys())[target_index]
            
            announce_identity(person_name, target_lang_code)
            sys.exit(0)
            
        except ValueError:
            print("Invalid input. Please enter a number.")
            sys.exit(1)

    # Handle standard text translation.
    input_text = sys.argv[1]
    
    print("Available Languages:")
    for i, lang_code in enumerate(SUPPORTED_LANGUAGES):
        print(f"    {i+1}. {SUPPORTED_LANGUAGES[lang_code]} ({lang_code})")

    try:
        source_index = int(input("\nEnter the number for your source language: ")) - 1
        target_index = int(input("Enter the number for your target language: ")) - 1
        
        if not (0 <= source_index < len(SUPPORTED_LANGUAGES) and 0 <= target_index < len(SUPPORTED_LANGUAGES)):
            print("Invalid language numbers. Please choose from the list.")
            sys.exit(1)

        source_lang_code = list(SUPPORTED_LANGUAGES.keys())[source_index]
        target_lang_code = list(SUPPORTED_LANGUAGES.keys())[target_index]
        source_lang_name = SUPPORTED_LANGUAGES[source_lang_code]
        target_lang_name = SUPPORTED_LANGUAGES[target_lang_code]

    except ValueError:
        print("Invalid input. Please enter a number.")
        sys.exit(1)
    
    translated_text = translate_text(input_text, source_lang_code, target_lang_code)
    print("Translated Text:", translated_text)
    
    if not translated_text.startswith("Error"):
        # Use gTTS for text-to-speech.
        audio_filename = text_to_speech_gtts(translated_text, target_lang_code)
        # Save translation to history.
        save_to_history_file("Text Translation", input_text, translated_text, source_lang_name, target_lang_name, audio_filename)

if __name__ == "__main__":
    main()


# import os
# import sys
# import requests
# from gtts import gTTS
# from dotenv import load_dotenv 
# from datetime import datetime
# import time
# import uuid

# # Load environment variables from a .env file.
# load_dotenv()

# # Get your API key from environment variables.
# API_KEY = os.getenv("API_KEY")
# if not API_KEY:
#     raise ValueError("API_KEY not found. Please set it as an environment variable or in a .env file.")
# API_URL_TEXT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

# # List of supported languages.
# SUPPORTED_LANGUAGES = {
#     "en": "English",
#     "kn": "Kannada",
#     "es": "Spanish",
#     "fr": "French",
#     "de": "German",
#     "ja": "Japanese",
#     "zh-CN": "Chinese (Simplified)",
#     "ru": "Russian",
#     "it": "Italian",
#     "pt": "Portuguese",
#     "ko": "Korean",
#     "ar": "Arabic",
#     "hi": "Hindi",
#     "tr": "Turkish",
# }

# def save_to_history_file(record_type, original_text, translated_text, source_lang, target_lang):
#     """Saves a new translation or announcement record to a local history.txt file."""
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     entry = (
#         f"[{timestamp}] Type: {record_type}\n"
#         f"Original Text: {original_text}\n"
#         f"Translated Text: {translated_text}\n"
#         f"Languages: {source_lang} -> {target_lang}\n"
#         "------------------------------------------\n"
#     )
#     with open("history.txt", "a", encoding="utf-8") as f:
#         f.write(entry)
#     print("Record saved to history.txt.")

# def text_to_speech_gtts(text, lang):
#     """
#     Converts text to speech, saves the audio file in the static/audio directory, and plays it.
#     """
#     print("Generating and playing audio...")
#     try:
#         tts = gTTS(text=text, lang=lang)
        
#         # Ensure the static/audio directory exists
#         audio_dir = os.path.join("static", "audio")
#         os.makedirs(audio_dir, exist_ok=True)

#         audio_filename = os.path.join(audio_dir, f"audio_{uuid.uuid4()}.mp3")
        
#         tts.save(audio_filename)
        
#         # This will play the audio file on most systems.
#         os.system(f"start {audio_filename}")
#         print(f"Audio file created and played: {audio_filename}")
        
#     except Exception as e:
#         print(f"Error during audio generation or playback: {e}")

# def translate_text(text, source_lang_code, target_lang_code):
#     """
#     Translates text from a source language to a target language using the Gemini API.
#     """
#     print("\nTranslating...")
#     prompt = f"Translate the following text from {source_lang_code} to {target_lang_code}: \"{text}\""

#     payload = {
#         "contents": [{"parts": [{"text": prompt}]}]
#     }

#     try:
#         response = requests.post(API_URL_TEXT, json=payload)
#         response.raise_for_status()
#         result = response.json()
#         translated_text = result['candidates'][0]['content']['parts'][0]['text']
#         return translated_text
#     except requests.exceptions.RequestException as e:
#         return f"Error during translation: {e}"
#     except (KeyError, IndexError) as e:
#         return f"Unexpected API response format: {e}"

# def announce_identity(person_name, lang):
#     """
#     Synthesizes and plays a voice message announcing a person's identity.
#     It also saves a record of the announcement to the history file.
#     The language is now determined by the user's input.
#     """
#     print(f"Announcing identity: {person_name} in {SUPPORTED_LANGUAGES[lang]}.")
#     text_to_announce = f"This is {person_name}."
    
#     # Generate and play the audio.
#     text_to_speech_gtts(text_to_announce, lang)
    
#     # Save the announcement to the history file.
#     save_to_history_file("Identity Announcement", person_name, text_to_announce, lang, lang)

# def main():
#     """Main function to handle command-line arguments and run the program."""
#     if len(sys.argv) < 2:
#         print("Usage: python translator_cli.py \"<text_to_translate>\"")
#         print("Or: python translator_cli.py --announce \"<person_name>\"")
#         sys.exit(1)

#     # Check for the identity announcement flag.
#     if sys.argv[1] == "--announce":
#         if len(sys.argv) < 3:
#             print("Please provide a name to announce.")
#             sys.exit(1)
        
#         person_name = sys.argv[2]
        
#         # Prompt the user to select a language for the announcement.
#         print("\nAvailable Languages for Announcement:")
#         for i, lang_code in enumerate(SUPPORTED_LANGUAGES):
#             print(f"    {i+1}. {SUPPORTED_LANGUAGES[lang_code]} ({lang_code})")
            
#         try:
#             target_index = int(input("\nEnter the number for your target language: ")) - 1
#             if not (0 <= target_index < len(SUPPORTED_LANGUAGES)):
#                 print("Invalid language number. Please choose from the list.")
#                 sys.exit(1)
#             target_lang_code = list(SUPPORTED_LANGUAGES.keys())[target_index]
            
#             announce_identity(person_name, target_lang_code)
#             sys.exit(0)
            
#         except ValueError:
#             print("Invalid input. Please enter a number.")
#             sys.exit(1)

#     # Handle standard text translation.
#     input_text = sys.argv[1]
    
#     print("Available Languages:")
#     for i, lang_code in enumerate(SUPPORTED_LANGUAGES):
#         print(f"    {i+1}. {SUPPORTED_LANGUAGES[lang_code]} ({lang_code})")

#     try:
#         source_index = int(input("\nEnter the number for your source language: ")) - 1
#         target_index = int(input("Enter the number for your target language: ")) - 1
        
#         if not (0 <= source_index < len(SUPPORTED_LANGUAGES) and 0 <= target_index < len(SUPPORTED_LANGUAGES)):
#             print("Invalid language numbers. Please choose from the list.")
#             sys.exit(1)

#         source_lang_code = list(SUPPORTED_LANGUAGES.keys())[source_index]
#         target_lang_code = list(SUPPORTED_LANGUAGES.keys())[target_index]
#         source_lang_name = SUPPORTED_LANGUAGES[source_lang_code]
#         target_lang_name = SUPPORTED_LANGUAGES[target_lang_code]

#     except ValueError:
#         print("Invalid input. Please enter a number.")
#         sys.exit(1)
    
#     translated_text = translate_text(input_text, source_lang_code, target_lang_code)
#     print("Translated Text:", translated_text)
    
#     if not translated_text.startswith("Error"):
#         # Use gTTS for text-to-speech.
#         text_to_speech_gtts(translated_text, target_lang_code)
#         # Save translation to history.
#         save_to_history_file("Text Translation", input_text, translated_text, source_lang_name, target_lang_name)

# if __name__ == "__main__":
#     main()
