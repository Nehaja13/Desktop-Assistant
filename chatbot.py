import streamlit as st
from llama_cpp import Llama
import sounddevice as sd
import numpy as np
import noisereduce as nr
import pyttsx3
from vosk import Model, KaldiRecognizer
import json
import queue
import threading

def chatbot_interface():
    # Load LLM model
    st.header("🤖 Offline Chatbot with Audio Analysis")
    
    # Initialize with default values
    llm = None
    vosk_model = None
    
    try:
        llm = Llama(
            model_path="C:/Users/Jammula Nehaja/Downloads/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",  # Update this path
            n_ctx=1024,
            n_threads=8,
            n_gpu_layers=20
        )
    except Exception as e:
        st.error(f"Failed to load LLM model: {str(e)}")
        return

    try:
        vosk_model = Model(r"C:/Users/Jammula Nehaja/OneDrive/Desktop/face_app/vosk-model-small-en-us-0.15")  # Update this path
    except Exception as e:
        st.error(f"Failed to load Vosk model: {str(e)}")
        return

    SYSTEM_PROMPT = "You are a helpful AI assistant. Provide concise, accurate responses."

    def chat_with_bot(prompt):
        try:
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
        except Exception as e:
            st.error(f"Error in chat_with_bot: {str(e)}")
            return "I encountered an error processing your request."

    # Audio processing queue for better performance
    audio_queue = queue.Queue()
    
    def record_audio(duration=6, sample_rate=16000):
        """Record audio with error handling"""
        try:
            st.info("🎙 Speak now or play audio near mic...")
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
        """Denoise and normalize audio"""
        try:
            if audio is None or len(audio) == 0:
                return audio
                
            if np.max(np.abs(audio)) == 0:
                return audio
                
            audio = audio / np.max(np.abs(audio))
            return nr.reduce_noise(y=audio, sr=sample_rate, prop_decrease=0.7)
        except Exception as e:
            st.warning(f"Audio enhancement error: {str(e)}")
            return audio

    def recognize_speech(audio, sample_rate):
        """Speech-to-text using Vosk"""
        if audio is None or len(audio) == 0:
            return None
            
        try:
            audio_int16 = (audio * 32767).astype(np.int16)
            recognizer = KaldiRecognizer(vosk_model, sample_rate)
            recognizer.SetWords(True)
            
            # Process in chunks for better performance
            chunk_size = 4000
            for i in range(0, len(audio_int16), chunk_size):
                chunk = audio_int16[i:i+chunk_size]
                recognizer.AcceptWaveform(chunk.tobytes())
                
            result = json.loads(recognizer.FinalResult())
            raw_text = result.get("text", "").strip()

            # Correction map (optional)
            corrections = {
                "what these by don": "what is Python",
                "what is by don": "what is Python",
                "what is john": "what is Python",
                "what is driver": "what is Java",
                "what is javan": "what is Java",
                "what is drama": "what is Java",
            }
            return corrections.get(raw_text.lower(), raw_text)
        except Exception as e:
            st.warning(f"Recognition error: {str(e)}")
            return None

    def text_to_speech(text):
        """Offline TTS with error handling"""
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            st.warning(f"TTS error: {str(e)}")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "voice_output" not in st.session_state:
        st.session_state.voice_output = True
    if "audio_memory" not in st.session_state:
        st.session_state.audio_memory = ""
    if "transcript_ready" not in st.session_state:
        st.session_state.transcript_ready = False
    if "audio_transcript" not in st.session_state:
        st.session_state.audio_transcript = ""

    # UI Controls
    st.session_state.voice_output = st.checkbox("🔊 Enable Voice Output", value=st.session_state.voice_output)

    col1, col2 = st.columns(2)

    # 🎤 Regular Voice Input
    if col1.button("🎤 Ask by Speaking"):
        audio, sr = record_audio()
        if audio is not None:
            st.audio(audio, sample_rate=sr)
            with st.spinner("Processing audio..."):
                cleaned = enhance_audio(audio, sr)
                transcript = recognize_speech(cleaned, sr)

                if transcript:
                    st.session_state.messages.append(("user", transcript))
                    with st.spinner("Thinking..."):
                        response = chat_with_bot(transcript)
                        st.session_state.messages.append(("bot", response))
                        if st.session_state.voice_output:
                            text_to_speech(response)
                else:
                    st.warning("Could not recognize your voice. Try again.")

    # 🎧 Audio Input (from device)
    if col2.button("🎧 Analyze Audio from Source"):
        audio, sr = record_audio(duration=10)
        if audio is not None:
            st.audio(audio, sample_rate=sr)
            with st.spinner("Processing audio..."):
                cleaned = enhance_audio(audio, sr)
                transcript = recognize_speech(cleaned, sr)

                if transcript:
                    st.success(f"🔎 Transcript: {transcript}")
                    st.session_state.audio_transcript = transcript
                    st.session_state.audio_memory = transcript
                    st.session_state.transcript_ready = True
                else:
                    st.warning("No speech detected. Try again with clearer audio.")

    # Follow-up question logic
    if st.session_state.transcript_ready:
        question = st.text_input("What do you want to ask about the audio?", key="audio_query_input")
        if question:
            full_query = f"Audio content: '{st.session_state.audio_transcript}'. Question: {question}"
            with st.spinner("Thinking..."):
                response = chat_with_bot(full_query)
                st.session_state.messages.append(("user", question))
                st.session_state.messages.append(("bot", response))
                if st.session_state.voice_output:
                    text_to_speech(response)

            # Reset the state
            st.session_state.transcript_ready = False
            st.session_state.audio_transcript = ""

    # Text Input
    user_input = st.chat_input("💬 Type your message...")
    if user_input:
        # Check if user is referring to previous audio
        if any(keyword in user_input.lower() for keyword in ["audio", "that", "what was said"]):
            if st.session_state.audio_memory:
                user_input = f"""User previously analyzed this audio: "{st.session_state.audio_memory}". 
Now respond to: {user_input}"""
            else:
                st.warning("No previous audio to reference")

        st.session_state.messages.append(("user", user_input))
        with st.spinner("Thinking..."):
            bot_response = chat_with_bot(user_input)
            st.session_state.messages.append(("bot", bot_response))
            if st.session_state.voice_output:
                text_to_speech(bot_response)

    # Chat Display
    for sender, message in st.session_state.messages:
        with st.chat_message(sender):
            st.markdown(message)

if __name__ == "__main__":
    chatbot_interface()
