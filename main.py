import sys
from pathlib import Path
import os
import subprocess
import webbrowser
import pyautogui
import speech_recognition as sr
import streamlit as st
from time import sleep
import ctypes
import psutil
import platform
from datetime import datetime
import json
import base64
import random
import pygame

# Initialize pygame for sounds
pygame.mixer.init()

sys.path.append(str(Path(__file__).parent))
from modules.command_executor import CommandExecutor
from config import FACE_DATASET_PATH, SCREENSHOTS_DIR
from face_gui import FaceAuthenticator
from ocr_exec import ocr_interface
from calorie_tracker import calorie_tracker_interface
from chatbot import chatbot_interface

# ===== Page Config (MUST BE FIRST) =====
st.set_page_config(
    page_title="✨ AI Desktop Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== Load Assets =====
def load_css():
    """Load CSS with theme variables"""
    css = Path("assets/style.css").read_text()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    # Apply current theme immediately
    if st.session_state.dark_mode:
        st.markdown("""
        <script>
        document.documentElement.setAttribute('data-theme', 'dark');
        </script>
        """, unsafe_allow_html=True)

def apply_theme():
    """Apply theme variables based on current mode"""
    theme = "dark" if st.session_state.dark_mode else "light"
    st.markdown(f"""
    <script>
    document.documentElement.setAttribute('data-theme', '{theme}');
    </script>
    """, unsafe_allow_html=True)

def toggle_dark_mode():
    """Toggle theme and force UI update"""
    st.session_state.dark_mode = not st.session_state.dark_mode
    apply_theme()
    st.rerun()

def render_theme_toggle():
    """Render theme toggle button with proper key management"""
    col1, col2 = st.columns([1,3])
    with col1:
        btn_label = "🌙" if not st.session_state.dark_mode else "☀️"
        if st.button(
            btn_label,
            key="theme_toggle_btn",  # Changed key to avoid duplicates
            help="Dark mode" if not st.session_state.dark_mode else "Light mode",
            use_container_width=True
        ):
            toggle_dark_mode()
    with col2:
        mode_text = "Dark Mode" if not st.session_state.dark_mode else "Light Mode"
        st.markdown(f"**{mode_text}**")

# ===== Audio Function =====
def autoplay_audio(file_path):
    """Play audio file automatically"""
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

# ===== Session State Initialization =====
def initialize_session_state():
    """Initialize all session state variables"""
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "sounds_on" not in st.session_state:
        st.session_state.sounds_on = True
    if "personality" not in st.session_state:
        st.session_state.personality = "professional"

# ===== App Initialization =====
def initialize_app():
    """Initialize the entire application"""
    initialize_session_state()
    load_css()
    apply_theme()

# Initialize the app
initialize_app()






# ===== Personality System =====
def load_personality():
    personalities = {
        "professional": {
            "name": "professional",
            "greeting": "AI Assistant ready to serve",
            "responses": {
                "hello": ["Hello. How may I assist you today?"],
                "error": ["I encountered an issue processing that request"]
            }
        },
        "friendly": {
            "name": "friendly",
            "greeting": "Hi there! How can I help? 😊",
            "responses": {
                "hello": ["Hey friend!", "Hi there! 😄"],
                "error": ["Oops! Something went wrong there"]
            }
        },
        "witty": {
            "name": "witty",
            "greeting": "Your witty assistant at your service! 🤪",
            "responses": {
                "hello": ["Ah, a human! How delightful!", "Greetings earthling!"],
                "error": ["My circuits got tangled on that one!"]
            }
        }
    }
    return personalities[st.session_state.personality]

# ===== UI Components =====
def show_confetti():
    st.components.v1.html("""
    <canvas id="confetti-canvas"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1"></script>
    <script>
    confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 }
    });
    </script>
    """, height=0)

def render_chat_message(role, content, timestamp):
    role_icon = "👤" if role == "user" else "🤖"
    bubble_class = "user-message" if role == "user" else "assistant-message"
    
    st.markdown(
        f'<div class="chat-message {bubble_class}">'
        f'{role_icon} {content}'
        f'<span class="message-time">{timestamp}</span>'
        '</div>',
        unsafe_allow_html=True
    )

def listen_for_command():
    """Listen for voice command using microphone"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.session_state.listening = True
        st.rerun()
        
        st.info("Listening... Speak now")
        if st.session_state.sounds_on:
            autoplay_audio("assets/sounds/wake.mp3")
            
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Could not request results"
        finally:
            st.session_state.listening = False
            st.rerun()

# ===== Command Processing =====
def execute_system_command(command):
    """Execute system commands with personality responses"""
    personality = load_personality()
    command = command.lower()
    
    try:
        # File Manager Commands
        if any(cmd in command for cmd in ["open file manager", "open files", "show files"]):
            if os.name == 'nt':
                os.startfile(os.environ['USERPROFILE'])
                return random.choice(personality["responses"]["hello"]) + " File manager opened"
            else:
                subprocess.run(['xdg-open', os.path.expanduser('~')])
                return random.choice(personality["responses"]["hello"]) + " File manager opened"
        
        # Browser Commands
        elif any(cmd in command for cmd in ["open browser", "open chrome", "open web browser"]):
            webbrowser.open('https://www.google.com')
            return "Browser opened successfully"
        
        # Terminal Commands
        elif any(cmd in command for cmd in ["open terminal", "open command prompt", "open cmd"]):
            if os.name == 'nt':
                os.system('start cmd')
            else:
                subprocess.run(['gnome-terminal'])
            return "Terminal opened"
        
        # Protected Resources
        elif "open notepad" in command:
            success, response = st.session_state.cmd_exec.execute_protected_action(
                st.session_state.face_auth, "Notepad"
            )
            return response
        
        elif "open whatsapp" in command:
            success, response = st.session_state.cmd_exec.execute_protected_action(
                st.session_state.face_auth, "WhatsApp"
            )
            return response
        
        # Screenshot command
        elif "take screenshot" in command:
            success, response = st.session_state.cmd_exec.take_screenshot()
            if success:
                try:
                    if os.name == 'nt':
                        os.startfile(response)
                    else:
                        subprocess.run(['xdg-open', response])
                except:
                    pass
            return response if success else f"Error: {response}"
        
        # System Power Commands
        elif any(cmd in command for cmd in ["shutdown", "shut down", "turn off"]):
            if os.name == 'nt':
                os.system("shutdown /s /t 1")
            else:
                subprocess.run(['shutdown', '-h', 'now'])
            return "System shutting down..."
        
        elif any(cmd in command for cmd in ["restart", "reboot"]):
            if os.name == 'nt':
                os.system("shutdown /r /t 1")
            else:
                subprocess.run(['shutdown', '-r', 'now'])
            return "System restarting..."
        
        elif any(cmd in command for cmd in ["lock screen", "lock computer"]):
            if os.name == 'nt':
                ctypes.windll.user32.LockWorkStation()
            else:
                subprocess.run(['gnome-screensaver-command', '-l'])
            return "Screen locked"
        
        else:
            return f"Command not recognized: {command}"
    
    except Exception as e:
        return random.choice(personality["responses"]["error"]) + f": {str(e)}"

# ===== Main Interfaces =====
def home_interface():
    """Enhanced home interface with all features"""
    personality = load_personality()
    
    # Display chat history
    for message in st.session_state.messages:
        render_chat_message(message["role"], message["content"], message["timestamp"])
    
    # Input area
    input_col, voice_col = st.columns([5, 1])
    
    with input_col:
        user_input = st.text_input(
            "Type your command...", 
            key="input",
            placeholder=f"Ask me anything ({st.session_state.personality} mode)"
        )
    
    with voice_col:
        voice_class = "voice-active" if getattr(st.session_state, 'listening', False) else ""
        if st.button(
            "🎤", 
            key="voice",
            help="Voice command",
            use_container_width=True
        ):
            command = listen_for_command()
            if command and "could not" not in command.lower():
                process_command(command)
    
    if user_input:
        process_command(user_input)
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    quick_cols = st.columns(4)
    with quick_cols[0]:
        if st.button("📂 File Manager", use_container_width=True):
            process_command("open file manager")
    with quick_cols[1]:
        if st.button("🌐 Browser", use_container_width=True):
            process_command("open chrome")
    with quick_cols[2]:
        if st.button("💻 Terminal", use_container_width=True):
            process_command("open terminal")
    with quick_cols[3]:
        if st.button("📷 Screenshot", use_container_width=True):
            process_command("take screenshot")
    
    # System controls
    st.subheader("⚙️ System Controls")
    sys_cols = st.columns(4)
    with sys_cols[0]:
        if st.button("🔌 Shutdown", use_container_width=True):
            process_command("shutdown")
    with sys_cols[1]:
        if st.button("🔄 Restart", use_container_width=True):
            process_command("restart")
    with sys_cols[2]:
        if st.button("💤 Sleep", use_container_width=True):
            st.warning("Sleep command not implemented yet")
    with sys_cols[3]:
        if st.button("🔒 Lock", use_container_width=True):
            process_command("lock screen")

def process_command(command):
    """Process and display command results"""
    if not command:
        return
    
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": command,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    
    # Play send sound
    if st.session_state.sounds_on:
        autoplay_audio("assets/sounds/send.mp3")
    
    # Process command
    with st.spinner("Processing..."):
        response = execute_system_command(command)
        
        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Trigger confetti for success
        if any(word in response.lower() for word in ["success", "opened", "unlocked"]):
            show_confetti()
    
    st.rerun()

# ===== Sidebar =====
def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Control Panel")
        
        # Personality Selector
        st.subheader("🎭 Personality")
        cols = st.columns(3)
        personalities = {
            "professional": {"icon": "👔", "desc": "Formal responses"},
            "friendly": {"icon": "😊", "desc": "Casual and warm"},
            "witty": {"icon": "🤪", "desc": "Funny and clever"}
        }
        
        for i, (name, data) in enumerate(personalities.items()):
            with cols[i]:
                if st.button(
                    data["icon"],
                    help=data["desc"],
                    key=f"personality_{name}",
                    use_container_width=True
                ):
                    st.session_state.personality = name
                    if st.session_state.sounds_on:
                        autoplay_audio("assets/sounds/notification.mp3")
                    st.rerun()
        
        # Navigation
        st.subheader("🧭 Navigation")
        app_mode = st.radio(
            "Features:",
            ["🏠 Home", "💬 Chatbot", "👤 Face Auth", "🔍 OCR", "🍏 Health"],
            key="app_mode",  # Critical: This maintains state
            label_visibility="collapsed"
        )
        
        # Command History
        if st.session_state.messages:
            st.subheader("🕒 History")
            for msg in reversed(st.session_state.messages[-10:]):
                if msg["role"] == "user":
                    st.markdown(
                        f'<div class="command-history-item">🗨️ {msg["content"]}</div>',
                        unsafe_allow_html=True
                    )
        
        # Settings
        st.subheader("⚙️ Settings")
        dark_col, sound_col = st.columns(2)
        with dark_col:
            if st.button(
                "🌙" if st.session_state.dark_mode else "☀️", 
                key="theme_toggle",
                help="Toggle dark mode",
                use_container_width=True
            ):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
        with sound_col:
            if st.button(
                "🔊" if st.session_state.sounds_on else "🔇", 
                key="sound_toggle",
                help="Toggle sounds",
                use_container_width=True
            ):
                st.session_state.sounds_on = not st.session_state.sounds_on
                st.rerun()

# ===== Main App =====
def main():
    # load_css()
    st.title("AI Desktop Assistant")
    render_sidebar()
    #render_theme_toggle()  # Call this where you want the toggle button
    
    # Apply theme
    if st.session_state.dark_mode:
        st.markdown("<style>[data-theme='dark'] {}</style>", unsafe_allow_html=True)
    
    # Route to selected interface
    if "app_mode" not in st.session_state:
        st.session_state.app_mode = "🏠 Home"
    
    if st.session_state.app_mode == "🏠 Home":
        home_interface()
    elif st.session_state.app_mode == "💬 Chatbot":
        chatbot_interface()
    elif st.session_state.app_mode == "👤 Face Auth":
        st.session_state.face_auth.authenticate()
    elif st.session_state.app_mode == "🔍 OCR":
        ocr_interface()
    elif st.session_state.app_mode == "🍏 Health":
        calorie_tracker_interface()

if __name__ == "__main__":
    main()
