# Voice Translation

A Python-based real-time voice translator that converts spoken language into another language and plays it back to the user. Designed for easy, interactive, and multi-directional communication.

---

## Features

### 1. Speech-to-Text
- Transcribes spoken words into text using the Google Web Speech API.
- First step in the translation pipeline, allowing the program to understand user input.

### 2. Speech-to-Speech Translation
- Translates recognized text into a target language using the `translate` library.
- Converts the translated text back into spoken audio using Google Text-to-Speech (`gTTS`).
- Enables seamless real-time voice translation.

### 3. Two-Way Communication *(Coming Soon)*
- Will enable conversation in both directions.
- The app will listen for speech in both source and target languages, translate, and speak them back.

---

## Getting Started

### Prerequisites

- Python 3.x
- A microphone connected to your computer

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/voice_translation.git
    cd voice_translation
    ```

2. **Install the required libraries:**
    ```bash
    pip install SpeechRecognition
    pip install translate
    pip install gTTS
    ```

---

## Usage

Run the script from your terminal:
```bash
python your_script_name.py
```
Follow the on-screen prompts to select your source and target languages and begin speaking.

---

## Supported Languages

- English (`en`)
- Spanish (`es`)
- French (`fr`)
- German (`de`)
- Japanese (`ja`)
- Hindi (`hi`)
- Russian (`ru`)
- Italian (`it`)
- Portuguese (`pt`)
- Korean (`ko`)
- Chinese (Mandarin) (`zh-CN`)
- Arabic (`ar`)

---

## Acknowledgements

- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [gTTS](https://pypi.org/project/gTTS/)
- [translate](https://pypi.org/project/translate/)
