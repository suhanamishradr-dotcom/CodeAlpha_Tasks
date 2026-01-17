# app.py
import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

# =======================
# PAGE CONFIG
# =======================
st.set_page_config(
    page_title="🌍 AI Voice Translator",
    page_icon="🌐",
    layout="centered"
)

# =======================
# CUSTOM CSS
# =======================
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #a1c4fd, #c2e9fb); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
.title {font-size: 48px; font-weight: bold; color: #0f1b4c; text-align: center; margin-bottom:0px;}
.subtitle {font-size: 20px; color: #1f3c88; text-align:center; margin-top:0px;margin-bottom:40px;}
.stTextInput>div>div>input, .stTextArea>div>div>textarea {border-radius:12px;padding:12px;border:2px solid #1f3c88;}
.stButton>button {border-radius:12px;padding:12px 24px;background: linear-gradient(90deg, #667eea, #764ba2);color:white;font-size:16px;font-weight:bold;transition: transform 0.2s;}
.stButton>button:hover {transform: scale(1.05); background: linear-gradient(90deg, #764ba2, #667eea);}
.card {background-color: rgba(255,255,255,0.85); border-radius:20px; padding:20px; box-shadow:0 8px 16px rgba(0,0,0,0.2);}
</style>
""", unsafe_allow_html=True)

# =======================
# HEADER
# =======================
st.markdown('<h1 class="title">🌍 AI Voice Translator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Translate text and hear it instantly!</p>', unsafe_allow_html=True)

# =======================
# GET SUPPORTED LANGUAGES FROM DEEP-TRANSLATOR
# =======================
# deep-translator does not provide a constant, so define all languages manually:
# You can get the official list from https://pypi.org/project/deep-translator/

supported_languages = {
    "Arabic": "ar", "Chinese": "zh", "English": "en", "French": "fr", "German": "de",
    "Hindi": "hi", "Italian": "it", "Japanese": "ja", "Korean": "ko", "Portuguese": "pt",
    "Russian": "ru", "Spanish": "es", "Turkish": "tr", "Vietnamese": "vi"
}
language_names = sorted(list(supported_languages.keys()))

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    text_input = st.text_area("Enter text to translate:", height=150)

    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("Source Language", language_names, index=language_names.index("English"))
    with col2:
        target_lang = st.selectbox("Target Language", language_names, index=language_names.index("Hindi"))

    if st.button("🌐 Translate"):
        if not text_input.strip():
            st.warning("Please enter some text to translate!")
        else:
            try:
                # Translate
                translated_text = GoogleTranslator(
                    source=supported_languages[source_lang],
                    target=supported_languages[target_lang]
                ).translate(text_input)

                st.success("Translation Successful ✅")

                # Show translated text
                st.markdown(f"**Translated Text ({target_lang}):**")
                st.text_area("Output", value=translated_text, height=150)

                # Copy guidance
                st.write("Copy text manually using Ctrl+C")

                # Text-to-Speech
                try:
                    tts = gTTS(text=translated_text, lang=supported_languages[target_lang])
                    with tempfile.NamedTemporaryFile(delete=True) as fp:
                        tts.save(fp.name + ".mp3")
                        st.audio(fp.name + ".mp3", format="audio/mp3")
                except Exception as e:
                    st.error(f"TTS not supported for this language: {e}")

            except Exception as e:
                st.error(f"Translation failed: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
