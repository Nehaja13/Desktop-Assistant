
import streamlit as st
st.set_page_config(
    page_title="AI Desktop Assistant",
    page_icon="🤖",
    layout="wide"
)

import os
import subprocess
import pyautogui
import speech_recognition as sr
import webbrowser
from time import sleep
from face_gui import FaceAuthenticator
import ctypes  # For Windows system commands
import psutil  # For battery information
import platform  # For system info
from pathlib import Path
from ocr_exec import ocr_interface
from calorie_tracker import calorie_tracker_interface
from chatbot import chatbot_interface

def load_css():
    css_file = Path("assets/style.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("CSS file not found!")

def initialize_app():
    css_file = Path("assets/style.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False

def load_nav_css():
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .nav-item {
        animation: fadeIn 0.5s ease-out forwards;
        opacity: 0;
    }
    .nav-item:nth-child(1) { animation-delay: 0.1s; }
    .nav-item:nth-child(2) { animation-delay: 0.3s; }
    .nav-item:nth-child(3) { animation-delay: 0.5s; }
    .nav-item:nth-child(4) { animation-delay: 0.7s; }
    .nav-item:nth-child(5) { animation-delay: 0.9s; }
    [data-testid="stSidebar"] {
        width: 300px !important;
    }
    .nav-item:hover {
        background-color: rgba(0,0,0,0.05);
        border-radius: 8px;
        transform: scale(1.02);
        transition: all 0.2s ease;
    }
    </style>
    """, unsafe_allow_html=True)

def create_nav_item(icon, text, delay=0):
    """Create an animated navigation item"""
    st.markdown(
        f"""
        <div class="nav-item" style="padding: 10px; margin: 5px 0; animation-delay: {delay}s">
            <span style="font-size: 24px; margin-right: 10px;">{icon}</span>
            <span style="font-size: 18px; vertical-align: middle;">{text}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    return st.empty()

if 'face_auth' not in st.session_state:
    st.session_state.face_auth = FaceAuthenticator("C:/Users/Jammula Nehaja/OneDrive/Desktop/mini proj/face_dataset")

PROTECTED_RESOURCES = {
    "Notepad": "notepad.exe",
    "WhatsApp": "whatsapp.exe",
    "Documents": r"C:/Users/Jammula Nehaja/Documents",
    "Project Files": r"C:/Users/Jammula Nehaja/OneDrive/Desktop/mini proj"
}

# ---- REPLACE HERE WITH FUNCTION CONTENT ----
# We'll insert the fixed versions of:
# - listen_for_command
# - execute_system_command
# - home_interface
# - process_command
# - handle_authentication_flow
# - navigation
# - main

# The remaining part will be appended in the next step

def listen_for_command():
    """Listen for voice command using microphone"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Could not request results"

def execute_system_command(command):
    """Execute basic system operations based on voice/text command"""
    command = command.lower()
    response = ""
    try:
        if any(cmd in command for cmd in ["open file manager", "open files", "show files"]):
            if os.name == 'nt':
                os.startfile(os.environ['USERPROFILE'])
                response = "File manager opened"
            else:
                subprocess.run(['xdg-open', os.path.expanduser('~')])
                response = "File manager opened"
        elif any(cmd in command for cmd in ["open browser", "open chrome", "open web browser"]):
            webbrowser.open('https://www.google.com')
            response = "Browser opened"
        elif "open terminal" in command or "open command prompt" in command:
            if os.name == 'nt':
                os.system('start cmd')
            else:
                subprocess.run(['gnome-terminal'])
            response = "Terminal opened"
        elif "open calculator" in command:
            if os.name == 'nt':
                os.system('calc')
            else:
                subprocess.run(['gnome-calculator'])
            response = "Calculator opened"
        else:
            response = f"Command not recognized: {command}"
    except Exception as e:
        response = f"Error executing command: {str(e)}"
    return response

def home_interface():
    """Enhanced home interface with voice and text input"""
    st.title("🌟 Your AI Desktop Assistant")
    st.write("Welcome to your personal assistant. How can I help you today?")

    with st.expander("💡 Available Commands"):
        st.write("""
        - **Protected Resources**: "open notepad", "open whatsapp" (require facial authentication)
        - **File Operations**: "open file manager", "show my files"
        - **Browser**: "open chrome", "open browser"
        - **Terminal**: "open terminal", "open command prompt"
        - **System**: "shutdown", "restart", "lock screen", "battery status"
        """)

    if 'auth_state' not in st.session_state:
        st.session_state.auth_state = {'in_progress': False, 'resource_name': None, 'command': None}

    input_option = st.radio("Choose input method:", ("Text", "Voice"))

    if input_option == "Text":
        command = st.text_input("Enter your command:", placeholder="e.g., 'open notepad'")
        if st.button("Submit") and command:
            process_command(command)
    else:
        if st.button("🎤 Start Voice Command"):
            with st.spinner("Listening..."):
                command = listen_for_command()
            if command:
                st.text_area("Heard command:", value=command, height=100, label_visibility="collapsed")
                if "could not" not in command.lower():
                    process_command(command)

    if st.session_state.auth_state['in_progress']:
        handle_authentication_flow()

    st.subheader("Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📂 Open File Manager"):
            process_command("open file manager")
    with col2:
        if st.button("🌐 Open Browser"):
            process_command("open chrome")
    with col3:
        if st.button("💻 Open Terminal"):
            process_command("open terminal")
    with col4:
        if st.button("📷 Take Screenshot"):
            process_command("take screenshot")

    st.subheader("System Controls")
    pc1, pc2, pc3, pc4 = st.columns(4)
    with pc1:
        if st.button("🔌 Shutdown"):
            process_command("shutdown")
    with pc2:
        if st.button("🔄 Restart"):
            process_command("restart")
    with pc3:
        if st.button("💤 Sleep"):
            process_command("sleep")
    with pc4:
        if st.button("🔒 Lock Screen"):
            process_command("lock screen")

def process_command(command):
    """Process the command and check if authentication is needed"""
    protected_resources = {
        "notepad": "Notepad",
        "whatsapp": "WhatsApp",
        "documents": "Documents",
        "project files": "Project Files"
    }
    for cmd, name in protected_resources.items():
        if cmd in command.lower():
            st.session_state.auth_state = {
                'in_progress': True,
                'resource_name': name,
                'command': command
            }
            st.rerun()
            return
    result = execute_system_command(command)
    st.success(result)

def handle_authentication_flow():
    """Handle the facial authentication flow"""
    auth_state = st.session_state.auth_state
    st.warning(f"🔒 Authentication required to access {auth_state['resource_name']}")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("❌ Cancel"):
            st.session_state.auth_state = {'in_progress': False, 'resource_name': None, 'command': None}
            st.rerun()
    with col2:
        if st.button("👤 Authenticate"):
            if st.session_state.face_auth.authenticate():
                st.success("✅ Authentication successful!")
                try:
                    path = PROTECTED_RESOURCES.get(auth_state['resource_name'])
                    if path.endswith(".exe"):
                        subprocess.Popen(path)
                    else:
                        os.startfile(path)
                    st.success(f"{auth_state['resource_name']} opened successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to open {auth_state['resource_name']}: {str(e)}")
                finally:
                    st.session_state.auth_state = {'in_progress': False, 'resource_name': None, 'command': None}
                    st.rerun()
            else:
                st.error("❌ Authentication failed. Please try again.")

def navigation():
    """Clean navigation without boxes"""
    with st.sidebar:
        st.markdown("<h2 style='margin-bottom: 20px;'>Navigation</h2>", unsafe_allow_html=True)
        nav_items = [
            ("🏠", "Home"),
            ("💬", "Chatbot"), 
            ("👤", "Face Auth"),
            ("🔍", "OCR"),
            ("🍏", "Health Tracker")
        ]
        for icon, text in nav_items:
            if st.button(f"{icon} {text}", key=f"nav_{text.lower().replace(' ', '_')}", help=f"Go to {text}"):
                st.session_state.current_page = text
                st.rerun()

def main():
    initialize_app()
    load_nav_css()
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    navigation()
    st.markdown("""
    <style>
    .page-content {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)
    with st.container():
        st.markdown(f"<div class='page-content'>", unsafe_allow_html=True)
        if st.session_state.current_page == "Home":
            home_interface()
        elif st.session_state.current_page == "Chatbot":
            chatbot_interface()
        elif st.session_state.current_page == "Face Auth":
            st.session_state.face_auth.authenticate()
        elif st.session_state.current_page == "OCR":
            ocr_interface()
        elif st.session_state.current_page == "Health Tracker":
            calorie_tracker_interface()
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
