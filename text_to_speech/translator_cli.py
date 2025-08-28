import os
import sys
import requests
from gtts import gTTS
from dotenv import load_dotenv 
load_dotenv()

# Get your API key from Google AI Studio.
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found. Please set it as an environment variable or in a .env file.")
API_URL_TEXT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

# List of supported languages for the user to choose from
SUPPORTED_LANGUAGES = [
    {"code": "en", "name": "English"},
    {"code": "kn", "name": "Kannada"},
    {"code": "es", "name": "Spanish"},
    {"code": "fr", "name": "French"},
    {"code": "de", "name": "German"},
    {"code": "ja", "name": "Japanese"},
    {"code": "zh", "name": "Chinese (Simplified)"},
    {"code": "ru", "name": "Russian"},
    {"code": "it", "name": "Italian"},
    {"code": "pt", "name": "Portuguese"},
    {"code": "ko", "name": "Korean"},
    {"code": "ar", "name": "Arabic"},
    {"code": "hi", "name": "Hindi"},
    {"code": "tr", "name": "Turkish"},
]

def translate_text(text, source_lang, target_lang):
    """
    Translates text from a source language to a target language using the Gemini API.
    """
    print("\nTranslating...")
    prompt = f"Translate the following text from {source_lang} to {target_lang}: \"{text}\""

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

def text_to_speech_gtts(text, lang):
    """
    Converts text to speech using gTTS and plays the audio file.
    """
    print("Generating and playing audio...")
    try:
        # Create a gTTS object with the translated text and target language
        tts = gTTS(text=text, lang=lang)
        
        # Define the temporary file path
        audio_file = "translated_audio.mp3"
        
        # Save the audio file
        tts.save(audio_file)
        print(f"Audio file created: {audio_file}")
        
        # Play the audio file using the OS's default player (Windows-specific)
        os.system(f"start {audio_file}")
        
    except Exception as e:
        print(f"Error during audio generation or playback: {e}")
    finally:
        # It's better to manually delete the file after playback is complete
        # to ensure it's not still in use by the OS.
        # For a simple script, leaving it for manual deletion is fine.
        pass

def main():
    """Main function to handle command-line arguments and run the program."""
    if len(sys.argv) < 2:
        print("Usage: python translator_cli.py \"<text_to_translate>\"")
        print("Example: python translator_cli.py \"Hello, how are you?\"")
        sys.exit(1)

    input_text = sys.argv[1]
    
    # Print the available languages
    print("Available Languages:")
    for i, lang in enumerate(SUPPORTED_LANGUAGES):
        print(f"  {i+1}. {lang['name']} ({lang['code']})")

    # Get user choice for source and target languages
    try:
        source_index = int(input("\nEnter the number for your source language: ")) - 1
        target_index = int(input("Enter the number for your target language: ")) - 1
        
        if not (0 <= source_index < len(SUPPORTED_LANGUAGES) and 0 <= target_index < len(SUPPORTED_LANGUAGES)):
            print("Invalid language numbers. Please choose from the list.")
            sys.exit(1)

        source_lang = SUPPORTED_LANGUAGES[source_index]['code']
        target_lang = SUPPORTED_LANGUAGES[target_index]['code']

    except ValueError:
        print("Invalid input. Please enter a number.")
        sys.exit(1)
    
    translated_text = translate_text(input_text, source_lang, target_lang)
    print("Translated Text:", translated_text)
    
    # Play the audio only if a valid translation was received
    if not translated_text.startswith("Error"):
        text_to_speech_gtts(translated_text, target_lang)

if __name__ == "__main__":
    main()























# import os
# import sys
# import requests
# import json
# import subprocess
# from pydub import AudioSegment, silence
# import io

# # ---
# # IMPORTANT: Before running, install the necessary libraries and audio player.
# # 
# # 1. Python libraries: `pip install requests pydub`
# #
# # 2. Audio Player: The script uses an external program to play audio.
# #    - On Windows, install FFmpeg and make sure `ffplay` is in your system's PATH.
# #      (Download FFmpeg from https://ffmpeg.org/download.html and add the bin directory to PATH)
# #    - On macOS/Linux, install FFmpeg (`brew install ffmpeg`) or `aplay` (`sudo apt-get install alsa-utils`).
# #      The script will automatically detect and try to use `ffplay`, `aplay`, or `vlc`.
# #
# # 3. Add your Gemini API Key below.
# # ---

# # Get your API key from Google AI Studio.
# API_KEY = "AIzaSyB2T32smEr1LSUHEVyH9f-LKr9HUnzk7zU"
# API_URL_TEXT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"
# API_URL_AUDIO = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={API_KEY}"

# # List of supported languages for the user to choose from
# SUPPORTED_LANGUAGES = [
#     {"code": "en", "name": "English"},
#     {"code": "es", "name": "Spanish"},
#     {"code": "fr", "name": "French"},
#     {"code": "de", "name": "German"},
#     {"code": "ja", "name": "Japanese"},
#     {"code": "zh", "name": "Chinese (Simplified)"},
#     {"code": "ru", "name": "Russian"},
#     {"code": "it", "name": "Italian"},
#     {"code": "pt", "name": "Portuguese"},
#     {"code": "ko", "name": "Korean"},
#     {"code": "ar", "name": "Arabic"},
#     {"code": "hi", "name": "Hindi"},
#     {"code": "tr", "name": "Turkish"},
# ]

# def find_audio_player():
#     """
#     Finds a suitable audio player available on the system, prioritizing VLC.
#     """
#     # Hardcoded path for VLC on a typical Windows installation
#     vlc_path_windows = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
#     if os.path.exists(vlc_path_windows):
#         return vlc_path_windows

#     # The original logic for other players
#     for player in ['vlc', 'ffplay', 'aplay']:
#         if os.system(f'command -v {player} >/dev/null 2>&1') == 0:
#             return player
#     return None

# def translate_text(text, source_lang, target_lang):
#     """
#     Translates text from a source language to a target language using the Gemini API.
    
#     Args:
#         text (str): The text to translate.
#         source_lang (str): The source language code (e.g., 'en').
#         target_lang (str): The target language code (e.g., 'es').
        
#     Returns:
#         str: The translated text or an error message.
#     """
#     print("\nTranslating...")
#     prompt = f"Translate the following text from {source_lang} to {target_lang}: \"{text}\""

#     payload = {
#         "contents": [{"parts": [{"text": prompt}]}]
#     }

#     try:
#         response = requests.post(API_URL_TEXT, json=payload)
#         response.raise_for_status()  # Raises an HTTPError for bad responses
#         result = response.json()
#         translated_text = result['candidates'][0]['content']['parts'][0]['text']
#         return translated_text
#     except requests.exceptions.RequestException as e:
#         return f"Error during translation: {e}"
#     except (KeyError, IndexError) as e:
#         return f"Unexpected API response format: {e}"

# def text_to_speech(text):
#     """
#     Converts text to speech, saves it as an MP3 file, and plays the MP3.
#     """
#     print("Generating and playing audio...")
#     payload = {
#         "contents": [{"parts": [{"text": text}]}],
#         "generationConfig": {
#             "responseModalities": ["AUDIO"],
#             "speechConfig": {
#                 "voiceConfig": {
#                     "prebuiltVoiceConfig": {"voiceName": "Kore"}
#                 }
#             }
#         },
#         "model": "gemini-2.5-flash-preview-tts"
#     }

#     try:
#         response = requests.post(API_URL_AUDIO, json=payload)
#         response.raise_for_status()
#         result = response.json()
        
#         audio_data_base64 = result['candidates'][0]['content']['parts'][0]['inlineData']['data']
#         audio_data = io.BytesIO(audio_data_base64.encode('utf-8'))

#         # The API returns raw PCM audio. Pydub is used to convert it into a playable format.
#         audio_segment = AudioSegment.from_file(audio_data, format="raw", frame_rate=16000, channels=1, sample_width=2)
        
#         # Define a temporary file path for the MP3
#         mp3_file = "translated_audio.mp3"
        
#         # Export the audio segment directly to MP3
#         audio_segment.export(mp3_file, format="mp3")
#         print(f"Final MP3 file created: {mp3_file}")
        
#         # Play the MP3 file using a suitable command-line tool
#         player = find_audio_player()
#         if not player:
#             print("Error: No suitable audio player found (ffplay, aplay, or vlc).")
#             return
        
#         player_args = [player, mp3_file]
#         if player == 'vlc':
#             player_args.extend(['--play-and-exit', '--no-video', '--qt-start-minimized'])

#         subprocess.run(player_args, check=True)
#         os.remove(mp3_file) # Clean up the final MP3 file

#     except requests.exceptions.RequestException as e:
#         print(f"Error during audio generation: {e}")
#     except (KeyError, IndexError) as e:
#         print(f"Unexpected audio API response format: {e}")
#     except subprocess.CalledProcessError:
#         print(f"Error: Failed to play audio with '{player}'. Make sure the player is correctly installed.")
#     """
#     Converts text to speech, saves it as a WAV file, converts the WAV to an MP3, and plays the MP3.
    
#     Args:
#         text (str): The text to convert to speech.
    
#     Returns:
#         None
#     """
#     print("Generating and playing audio...")
#     payload = {
#         "contents": [{"parts": [{"text": text}]}],
#         "generationConfig": {
#             "responseModalities": ["AUDIO"],
#             "speechConfig": {
#                 "voiceConfig": {
#                     # Change the voice here!
#                     # You can choose from various voices with distinct characteristics:
#                     # 'Zephyr' (Bright), 'Puck' (Upbeat), 'Charon' (Informative),
#                     # 'Kore' (Firm), 'Fenrir' (Excitable), 'Leda' (Youthful),
#                     # 'Orus' (Firm), 'Aoede' (Breezy), 'Callirrhoe' (Easy-going),
#                     # 'Autonoe' (Bright), 'Enceladus' (Breathy), 'Iapetus' (Clear),
#                     # 'Umbriel' (Easy-going), 'Algieba' (Smooth), 'Despina' (Smooth),
#                     # 'Erinome' (Clear), 'Algenib' (Gravelly), 'Rasalgethi' (Informative),
#                     # 'Laomedeia' (Upbeat), 'Achernar' (Soft), 'Alnilam' (Firm),
#                     # 'Schedar' (Even), 'Gacrux' (Mature), 'Pulcherrima' (Forward),
#                     # 'Achird' (Friendly), 'Zubenelgenubi' (Casual), 'Vindemiatrix' (Gentle),
#                     # 'Sadachbia' (Lively), 'Sadaltager' (Knowledgeable), 'Sulafat' (Warm).
#                     "prebuiltVoiceConfig": {"voiceName": "Kore"}
#                 }
#             }
#         },
#         "model": "gemini-2.5-flash-preview-tts"
#     }

#     try:
#         response = requests.post(API_URL_AUDIO, json=payload)
#         response.raise_for_status()
#         result = response.json()
        
#         audio_data_base64 = result['candidates'][0]['content']['parts'][0]['inlineData']['data']
#         audio_data = io.BytesIO(audio_data_base64.encode('utf-8'))

#         # The API returns raw PCM audio. Pydub is used to convert it into a playable format.
#         audio_segment = AudioSegment.from_file(audio_data, format="raw", frame_rate=16000, channels=1, sample_width=2)
        
#         # Define a temporary file paths
#         wav_file = "translated_audio.wav"
#         mp3_file = "translated_audio.mp3"
        
#         # First, export to WAV
#         audio_segment.export(wav_file, format="wav")
#         print(f"Intermediate WAV file created: {wav_file}")
        
#         # Second, convert the WAV file to MP3
#         audio_segment.export(mp3_file, format="mp3")
#         print(f"Final MP3 file created: {mp3_file}")
        
#         # Play the MP3 file using a suitable command-line tool
#         player = find_audio_player()
#         if not player:
#             print("Error: No suitable audio player found (ffplay, aplay, or vlc).")
#             return
        
#         # Add flags for VLC to ensure it plays and exits without a GUI
#         player_args = [player, mp3_file]
#         if player == 'vlc':
#             player_args.extend(['--play-and-exit', '--no-video', '--qt-start-minimized'])

#         subprocess.run(player_args, check=True)
#         os.remove(wav_file) # Clean up the temporary WAV file
#         os.remove(mp3_file) # Clean up the final MP3 file

#     except requests.exceptions.RequestException as e:
#         print(f"Error during audio generation: {e}")
#     except (KeyError, IndexError) as e:
#         print(f"Unexpected audio API response format: {e}")
#     except subprocess.CalledProcessError:
#         print(f"Error: Failed to play audio with '{player}'. Make sure the player is correctly installed.")

# def main():
#     """Main function to handle command-line arguments and run the program."""
#     if len(sys.argv) < 2:
#         print("Usage: python translator_cli.py \"<text_to_translate>\"")
#         print("Example: python translator_cli.py \"Hello, how are you?\"")
#         sys.exit(1)

#     input_text = sys.argv[1]
    
#     # Print the available languages
#     print("Available Languages:")
#     for i, lang in enumerate(SUPPORTED_LANGUAGES):
#         print(f"  {i+1}. {lang['name']} ({lang['code']})")

#     # Get user choice for source and target languages
#     try:
#         source_index = int(input("\nEnter the number for your source language: ")) - 1
#         target_index = int(input("Enter the number for your target language: ")) - 1
        
#         if not (0 <= source_index < len(SUPPORTED_LANGUAGES) and 0 <= target_index < len(SUPPORTED_LANGUAGES)):
#             print("Invalid language numbers. Please choose from the list.")
#             sys.exit(1)

#         source_lang = SUPPORTED_LANGUAGES[source_index]['code']
#         target_lang = SUPPORTED_LANGUAGES[target_index]['code']

#     except ValueError:
#         print("Invalid input. Please enter a number.")
#         sys.exit(1)
    
#     translated_text = translate_text(input_text, source_lang, target_lang)
#     print("Translated Text:", translated_text)
    
#     # Play the audio only if a valid translation was received
#     if not translated_text.startswith("Error"):
#         text_to_speech(translated_text)

# if __name__ == "__main__":
#     main()
