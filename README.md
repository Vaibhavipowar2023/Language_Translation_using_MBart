# Language Translation using mBART

This project demonstrates a **Language Translation App** using the **mBART** model (Multilingual BART) for neural machine translation. The app supports multiple languages and allows users to translate text and listen to the translated result using Text-to-Speech.

## Features

- **Language Translation**: Translate text between multiple languages, including English, Hindi, Marathi, French, Spanish, and German.
- **Speech-to-Text**: Allow users to speak the text for translation through the microphone.

## Supported Languages

- English
- Hindi
- Marathi 
- French 
- Spanish 
- German 
## Requirements

- Python 3.x
- Streamlit
- Transformers
- PyTorch
- pyttsx3 (for Text-to-Speech)
- SpeechRecognition (for Speech-to-Text)
- Pickle (for saving and loading models and tokenizers)

## Example
### Input

**Source Language:** English

**Target Language:** Hindi

**Text:** "Hello, how are you?"

### Output

**Translated Text:** "नमस्ते, आप कैसे हैं?"

