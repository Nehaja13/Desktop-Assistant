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

# Add project root to Python path
sys.path.append(str(Path(__file__).parent))

# Now your imports will work
from modules.command_executor import CommandExecutor
from config import FACE_DATASET_PATH, SCREENSHOTS_DIR
from face_gui import FaceAuthenticator

# Import other module interfaces
from ocr_exec import ocr_interface
from calorie_tracker import calorie_tracker_interface
from chatbot import chatbot_interface

# Set page config MUST be the first Streamlit command
st.set_page_config(
    page_title="AI Desktop Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize in session state
if 'command_executor' not in st.session_state:
    st.session_state.cmd_exec = CommandExecutor()
if 'face_auth' not in st.session_state:
    st.session_state.face_auth = FaceAuthenticator("C:/Users/Jammula Nehaja/OneDrive/Desktop/mini proj/face_dataset")

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
    """Updated to use CommandExecutor"""
    command = command.lower()
    
    try:
        # File Manager Commands
        if any(cmd in command for cmd in ["open file manager", "open files", "show files"]):
            if os.name == 'nt':
                os.startfile(os.environ['USERPROFILE'])
                return "File manager opened"
            else:
                subprocess.run(['xdg-open', os.path.expanduser('~')])
                return "File manager opened"
        
        # Browser Commands
        elif any(cmd in command for cmd in ["open browser", "open chrome", "open web browser"]):
            webbrowser.open('https://www.google.com')
            return "Browser opened"
        
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
        return f"Error executing command: {str(e)}"

def home_interface():
    """Enhanced home interface with voice and text input"""
    st.title("🌟 Your AI Desktop Assistant")
    st.write("Welcome to your personal assistant. How can I help you today?")
    
    # Display command examples
    with st.expander("💡 Available Commands"):
        st.write("""
        - **File Operations**: "open file manager", "show my files"
        - **Browser**: "open chrome", "open browser"
        - **Terminal**: "open terminal", "open command prompt"
        - **Applications**: "open notepad", "open calculator"
        - **System**: 
            - "take screenshot", "system info"
            - "shutdown", "restart", "sleep"
            - "lock screen", "battery status"
        """)
    
    # Input options
    input_option = st.radio("Choose input method:", ("Text", "Voice"))
    
    command = ""
    if input_option == "Text":
        command = st.text_input("Enter your command:", placeholder="e.g., 'open file manager'")
        if st.button("Submit") and command:
            result = execute_system_command(command)
            st.success(result)
    else:
        if st.button("🎤 Start Voice Command"):
            with st.spinner("Listening..."):
                command = listen_for_command()
            if command:
                st.text_area("Heard command:", value=command, height=100, 
                           placeholder="Your voice command will appear here...",
                           label_visibility="collapsed")
                if "could not" not in command.lower():
                    result = execute_system_command(command)
                    st.success(result)
    
    # Quick access buttons
    st.subheader("Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📂 Open File Manager"):
            result = execute_system_command("open file manager")
            st.success(result)
    with col2:
        if st.button("🌐 Open Browser"):
            result = execute_system_command("open chrome")
            st.success(result)
    with col3:
        if st.button("💻 Open Terminal"):
            result = execute_system_command("open terminal")
            st.success(result)
    with col4:
        if st.button("📷 Take Screenshot"):
            result = execute_system_command("take screenshot")
            st.success(result)
    
    # System Power Buttons (in a new row)
    st.subheader("System Controls")
    power_col1, power_col2, power_col3, power_col4 = st.columns(4)
    with power_col1:
        if st.button("🔌 Shutdown", help="Shutdown the computer"):
            result = execute_system_command("shutdown")
            st.success(result)
    with power_col2:
        if st.button("🔄 Restart", help="Restart the computer"):
            result = execute_system_command("restart")
            st.success(result)
    with power_col3:
        if st.button("💤 Sleep", help="Put computer to sleep"):
            result = execute_system_command("sleep")
            st.success(result)
    with power_col4:
        if st.button("🔒 Lock Screen", help="Lock the computer"):
            result = execute_system_command("lock screen")
            st.success(result)

def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio(
        "Choose a feature:",
        ["🏠 Home", "💬 Chatbot", "👤 Face Auth", "🔍 OCR", "🍏 Health Tracker"]
    )
    
    if app_mode == "🏠 Home":
        home_interface()
    elif app_mode == "💬 Chatbot":
        chatbot_interface()
    elif app_mode == "👤 Face Auth":
        st.session_state.face_auth.authenticate()  # Direct access to auth interface
    elif app_mode == "🔍 OCR":
        ocr_interface()
    elif app_mode == "🍏 Health Tracker":
        calorie_tracker_interface()

if __name__ == "__main__":
    main()
