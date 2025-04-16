
    
#211 
    
'''import streamlit as st
from llama_cpp import Llama
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import pyttsx3
import noisereduce as nr
import tempfile
import os

def chatbot_interface(conn=None):
    # Load the model only when needed
    llm = Llama(
        model_path="C:/Users/Jammula Nehaja/Downloads/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        n_ctx=1024,
        n_threads=8,
        n_gpu_layers=20
    )
    
    SYSTEM_PROMPT = """You are a helpful AI assistant. Provide concise, accurate responses. 
    If you don't know something, say so."""
    
    def chat_with_bot(prompt):
        full_prompt = f"""<|system|>
    {SYSTEM_PROMPT}</s>
    <|user|>
    {prompt}</s>
    <|assistant|>
    """
        response = llm(
            full_prompt,
            max_tokens=256,
            temperature=0.5,
            top_p=0.7,
            repeat_penalty=1.1,
            stop=["</s>", "<|user|>"]
        )
        text = response["choices"][0]["text"].strip()
        for stop in ["<|system|>", "<|user|>"]:
            text = text.split(stop)[0]
        return text
    
    # Speech recognition functions
    def record_audio(duration=5, sample_rate=44100):
        
        try:
            st.info(f"Recording for {duration} seconds... Speak now!")
            audio = sd.rec(int(duration * sample_rate), 
                        samplerate=sample_rate, 
                        channels=1, 
                        dtype='float32')
            sd.wait()
            return audio.flatten(), sample_rate
        except Exception as e:
            st.error(f"Recording failed: {str(e)}")
            return None, None
    
    def reduce_noise(audio, sample_rate):
        """Apply noise reduction to audio"""
        return nr.reduce_noise(y=audio, sr=sample_rate)
    
    def recognize_speech(audio, sample_rate):
        if audio is None:
            return "No audio recorded"
        
        recognizer = sr.Recognizer()
        temp_file = None
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                temp_file = tmpfile.name
                wav.write(temp_file, sample_rate, (audio * 32767).astype(np.int16))
            
            # Process audio
            with sr.AudioFile(temp_file) as source:
                audio_data = recognizer.record(source)
                try:
                    return recognizer.recognize_google(audio_data)
                except sr.UnknownValueError:
                    return "Could not understand audio"
                except sr.RequestError as e:
                    return f"API Error: {str(e)}"
        except Exception as e:
            st.error(f"Speech recognition error: {str(e)}")
            return "Processing error"
        finally:
            # Clean up temp file
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass  # File will be cleaned up by system eventually
    
    def text_to_speech(text):
        """Convert text to speech"""
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume level
        engine.say(text)
        engine.runAndWait()
    
    # Chatbot UI
    st.title("🤖 Offline Chatbot with Voice")
    
    # Voice input/output controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎤 Voice Input"):
            audio, sample_rate = record_audio()
            cleaned_audio = reduce_noise(audio, sample_rate)
            user_input = recognize_speech(cleaned_audio, sample_rate)
            if user_input and user_input not in ["Could not understand audio", "API unavailable"]:
                st.session_state.voice_input = user_input
    
    with col2:
        voice_output = st.checkbox("🔊 Voice Output", value=False)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Check for voice input
    if "voice_input" in st.session_state and st.session_state.voice_input:
        user_input = st.session_state.voice_input
        del st.session_state.voice_input
    else:
        user_input = st.chat_input("Your message (or use voice input):")
    
    if user_input:
        st.session_state.messages.append(("user", user_input))
        with st.spinner("Thinking..."):
            try:
                bot_response = chat_with_bot(user_input)
                st.session_state.messages.append(("bot", bot_response))
                
                # Voice output if enabled
                if voice_output:
                    with st.spinner("Generating voice response..."):
                        text_to_speech(bot_response)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display messages
    for sender, msg in st.session_state.messages:
        if sender == "user":
            with st.chat_message("user"):
                st.write(msg)
        else:
            with st.chat_message("assistant"):
                st.write(msg)

# For standalone execution
if __name__ == "__main__":
    st.set_page_config(page_title="Offline Chatbot with Voice")
    chatbot_interface()'''
    
    
    
#pip install vosk sounddevice noisereduce pyttsx3 
import streamlit as st
from llama_cpp import Llama
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import pyttsx3
import noisereduce as nr
import tempfile
import os
from vosk import Model, KaldiRecognizer
import json

def chatbot_interface():
    # Load LLM model
    llm = Llama(
        model_path="C:/Users/Jammula Nehaja/Downloads/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        n_ctx=1024,
        n_threads=8,
        n_gpu_layers=20
    )
    
    # Load Vosk model (place in project directory)
    vosk_model = Model(r"C:/Users/Jammula Nehaja/OneDrive/Desktop/mini proj/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15")  # Update path
    
    SYSTEM_PROMPT = """You are a helpful AI assistant. Provide concise, accurate responses."""
    
    def chat_with_bot(prompt):
        full_prompt = f"""<|system|>{SYSTEM_PROMPT}</s><|user|>{prompt}</s><|assistant|>"""
        response = llm(
            full_prompt,
            max_tokens=256,
            temperature=0.5,
            top_p=0.7,
            repeat_penalty=1.1,
            stop=["</s>", "<|user|>"]
        )
        return response["choices"][0]["text"].strip().split("<|")[0]
    
    def record_audio(duration=4, sample_rate=16000):
        """Record audio optimized for speech recognition"""
        try:
            st.info("Speak now...")
            audio = sd.rec(int(duration * sample_rate),
                         samplerate=sample_rate,
                         channels=1,
                         dtype='float32')
            sd.wait()
            return audio.flatten(), sample_rate
        except Exception as e:
            st.error(f"Recording error: {str(e)}")
            return None, None
    
    def enhance_audio(audio, sample_rate):
        """Audio processing pipeline"""
        try:
            audio = audio / np.max(np.abs(audio))  # Normalize
            return nr.reduce_noise(y=audio, sr=sample_rate, prop_decrease=0.7)
        except:
            return audio
    
    def recognize_speech(audio, sample_rate):
        """Offline recognition with Vosk"""
        if audio is None:
            return None
        
        try:
            # Convert to 16-bit PCM
            audio_int16 = (audio * 32767).astype(np.int16)
            
            # Initialize recognizer
            recognizer = KaldiRecognizer(vosk_model, sample_rate)
            recognizer.AcceptWaveform(audio_int16.tobytes())
            
            # Get final result
            result = json.loads(recognizer.FinalResult())
            raw_text = result.get("text", "")
            
            # Text correction for common mistakes
            corrections = {
                "what these by don": "what is Python",
                "what is by don": "what is Python",
                "what is john": "what is Python",
                "what is java": "what is Java"
            }
            return corrections.get(raw_text.lower(), raw_text)
        except:
            return None
    
    def text_to_speech(text):
        """Offline text-to-speech"""
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.say(text)
            engine.runAndWait()
        except:
            pass
    
    # UI Setup
    st.title("🤖 Fully Offline Chatbot")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Voice Input
    if st.button("🎤 Voice Input"):
        audio, sr = record_audio()
        if audio is not None:
            st.audio(audio, sample_rate=sr)
            cleaned_audio = enhance_audio(audio, sr)
            user_input = recognize_speech(cleaned_audio, sr)
            
            if user_input:
                st.session_state.messages.append(("user", user_input))
                with st.spinner("Thinking..."):
                    bot_response = chat_with_bot(user_input)
                    st.session_state.messages.append(("bot", bot_response))
                    
                    if st.session_state.get("voice_output", False):
                        text_to_speech(bot_response)
            else:
                st.warning("Could not understand audio")
    
    # Text Input
    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state.messages.append(("user", user_input))
        with st.spinner("Thinking..."):
            bot_response = chat_with_bot(user_input)
            st.session_state.messages.append(("bot", bot_response))
            
            if st.session_state.get("voice_output", False):
                text_to_speech(bot_response)
    
    # Voice Output Toggle
    st.session_state.voice_output = st.checkbox("🔊 Voice Output")
    
    # Display Messages
    for sender, message in st.session_state.messages:
        with st.chat_message(sender):
            st.write(message)

if __name__ == "__main__":
    st.set_page_config(page_title="Offline Chatbot")
    chatbot_interface()























   
    








# import streamlit as st
# from llama_cpp import Llama

# # Load the model (moved inside the function to avoid loading when imported)
# SYSTEM_PROMPT = """You are a helpful AI assistant. Provide concise, accurate responses. 
# If you don't know something, say so."""

# def chatbot_interface(conn=None):
#     # Initialize the model only when the chatbot interface is actually used
#     llm = Llama(
#         model_path="C:/Users/Jammula Nehaja/Downloads/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
#         n_ctx=1024,
#         n_threads=8,
#         n_gpu_layers=20
#     )

#     def chat_with_bot(prompt):
#         full_prompt = f"""<|system|>
#     {SYSTEM_PROMPT}</s>
#     <|user|>
#     {prompt}</s>
#     <|assistant|>
#     """
#         response = llm(
#             full_prompt,
#             max_tokens=256,
#             temperature=0.5,
#             top_p=0.7,
#             repeat_penalty=1.1,
#             stop=["</s>", "<|user|>"]
#         )
#         text = response["choices"][0]["text"].strip()
#         for stop in ["<|system|>", "<|user|>"]:
#             text = text.split(stop)[0]
#         return text

#     # Streamlit UI
#     st.title("🤖 Offline Chatbot")
    
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     user_input = st.chat_input("Your message:")

#     if user_input:
#         st.session_state.messages.append(("user", user_input))
        
#         with st.spinner("Thinking..."):
#             try:
#                 bot_response = chat_with_bot(user_input)
#                 st.session_state.messages.append(("bot", bot_response))
#             except Exception as e:
#                 st.error(f"Error: {str(e)}")

#     # Display messages
#     for sender, msg in st.session_state.messages:
#         if sender == "user":
#             with st.chat_message("user"):
#                 st.write(msg)
#         else:
#             with st.chat_message("assistant"):
#                 st.write(msg)

# # This allows the file to be run standalone
# if __name__ == "__main__":
#     st.set_page_config(page_title="Offline Chatbot")  # Only for standalone use
#     chatbot_interface()