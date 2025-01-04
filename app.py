import streamlit as st
import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import pickle
import pyttsx3  # Text-to-Speech
import speech_recognition as sr  # Speech-to-Text

# Load the tokenizer
with open('tokenizer.pkl', 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

# Load the model
model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
model.eval()  # Set model to evaluation mode

# Streamlit app configuration
st.set_page_config(page_title="Language Translation App", layout="centered")

# Injecting custom CSS
st.markdown("""
    <style>
        body {
            font-family: 'Courier New', Courier, monospace;
        }
        .stButton button {
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        .stTextInput, .stTextArea {
            font-size: 16px;
            border-radius: 5px;
            padding: 10px;
            width: 100%;
        }
        .center-text {
            text-align: center;
            margin-top: 20px;
            font-size: 20px;
            font-weight: bold;
            font-color : black;
        }
        .translated-box {
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            
        }
    </style>
""", unsafe_allow_html=True)

# Title with an icon
st.title("Language Translation App")
st.write("🔄 Translate text between multiple languages and listen to translations.")

# Language flags for visual appeal
language_flags = {
    "en_XX": "English",
    "hi_IN": "Hindi",
    "mr_IN": "Marathi",
    "fr_XX": "French",
    "es_XX": "Spanish",
    "de_DE": "German"
}

# Layout: Create two columns for source and target language
col1, col2 = st.columns([1, 1])

# Input fields for source and target language
with col1:
    source_lang = st.selectbox(
        "Select Source Language",
        options=["Select Language", "en_XX", "hi_IN", "mr_IN", "fr_XX", "es_XX", "de_DE"],
        format_func=lambda x: language_flags.get(x, x),
    )

with col2:
    target_lang = st.selectbox(
        "Select Target Language",
        options=["Select Language", "en_XX", "hi_IN", "mr_IN", "fr_XX", "es_XX", "de_DE"],
        format_func=lambda x: language_flags.get(x, x),
    )

# Text input area
text_to_translate = st.text_area("Enter text to translate", height=100)

# Function for translation
def translate(text, source_lang, target_lang):
    if not text.strip():
        st.error("Please enter a valid text to translate.")
        return ""

    if source_lang == "Select Language":
        st.error("Please select a source language.")
        return ""

    if target_lang == "Select Language":
        st.error("Please select a target language.")
        return ""

    tokenizer.src_lang = source_lang
    model_inputs = tokenizer(text, return_tensors="pt")

    # Translate text
    translated = model.generate(
        **model_inputs, forced_bos_token_id=tokenizer.lang_code_to_id[target_lang]
    )
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

    return translated_text

# Text-to-Speech for translation
def speak_translation(translation):
    engine = pyttsx3.init()
    engine.say(translation)
    engine.runAndWait()

# Speech-to-Text for voice input
def listen_for_input():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("🎙️ Listening... Please speak.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand your speech.")
            return ""
        except sr.RequestError:
            st.error("Could not request results. Please check your internet connection.")
            return ""

# Buttons for actions
button_col1, button_col2 = st.columns([1, 1])

# Button for voice input
with button_col1:
    if st.button("🎤 Speak to Translate"):
        text_to_translate = listen_for_input()
        if text_to_translate:
            st.session_state.text_to_translate = text_to_translate

# Button for translation
if st.button("🔄 Translate"):
    if not text_to_translate.strip():
        st.error("Please enter text to translate.")
    elif source_lang == target_lang:
        st.error("Source and target languages must be different.")
    else:
        try:
            translation = translate(text_to_translate, source_lang, target_lang)
            st.success("Translation Successful!")
            
            # Display translated text outside the columns
            st.markdown(
                f"""
                <div class="center-text" >
                    Translated Text:
                    <div class="translated-box">{translation}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            # Text-to-Speech
            speak_translation(translation)
        except Exception as e:
            st.error(f"An error occurred during translation: {str(e)}")


