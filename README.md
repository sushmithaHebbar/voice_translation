# voice_translation
Speech to Text: Python tool using Google's API to convert spoken words into text.  Speech to Speech: A translator that listens, translates to a chosen language, and then speaks the translation aloud.  Two-Way Translator: An enhanced tool for seamless, two-way communication between people speaking different languages.

Real-Time Language Translator
This is a Python-based real-time voice translator that converts spoken language into another language and plays it back to the user. It's built to facilitate easy, interactive, and multi-directional communication across language barriers.

Features
1. Speech-to-Text
This core functionality transcribes spoken words into text using the Google Web Speech API. It's the first step in the translation pipeline, allowing the program to understand user input.

2. Speech-to-Speech Translation
The application translates recognized text into a target language using the translate library, then converts the translated text back into spoken audio using Google Text-to-Speech (gTTS). This creates a complete speech-to-speech translation loop.

3. Two-Way Communication (Coming Soon)
This feature will enhance the translator to handle a conversation in both directions. The application will listen for speech in both the source and target languages, translating and speaking them back in real-time. This is ideal for two-person conversations where each person speaks a different language.

Getting Started

Prerequisites:

Python 3.x

A microphone connected to your computer

Installation:

Clone the repository:

git clone https://github.com/your-username/voice_translation.git
cd your-repo-name

Install the required libraries:

pip install SpeechRecognition
pip install translate
pip install gTTS

Usage
Run the script from your terminal:

python your_script_name.py
Follow the on-screen prompts to select your source and target languages and begin speaking.

Supported Languages
The application supports the following languages:

English (en)

Spanish (es)

French (fr)

German (de)

Japanese (ja)

Hindi (hi)

Russian (ru)

Italian (it)

Portuguese (pt)

Korean (ko)

Chinese (Mandarin) (zh-CN)

Arabic (ar)

