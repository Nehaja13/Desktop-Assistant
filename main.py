import streamlit as st
st.set_page_config(
    page_title="AI Desktop Assistant",
    page_icon="🤖",
    layout="wide"
)

# Then other imports
import os
import time
import threading
import queue
import subprocess
import pyautogui
import speech_recognition as sr
import webbrowser
from time import sleep
import ctypes
import psutil
import platform

# Local imports (create these files if missing)
from ocr_exec import ocr_interface
from calorie_tracker import calorie_tracker_interface
from chatbot import chatbot_interface
from face_gui import FaceAuthenticator, protect_resource

# Move FaceAuthenticator class here temporarily to avoid circular imports
class FaceAuthenticator:
    def __init__(self, database_path):
        self.database_path = database_path
        self.result_queue = queue.Queue()
        self.authenticated = False
        self.authenticated_user = None
        self.auth_timeout = 1800
        self.last_auth_time = 0
    
    def authenticate(self):
        if self.is_session_valid():
            return True
            
        st.title("🔒 Face Authentication Required")
        with st.expander("Authentication Panel", expanded=True):
            st.write("Please authenticate using facial recognition to continue")
            
            if st.button("Start Face Recognition"):
                with st.spinner("Initializing camera..."):
                    self.reset_authentication()
                    
                    # Start recognition thread
                    recognition_thread = threading.Thread(
                        target=self.run_recognition,
                        daemon=True
                    )
                    recognition_thread.start()
                    
                    # Create UI elements
                    status = st.empty()
                    log = st.empty()
                    camera_placeholder = st.empty()
                    messages = []
                    
                    # Process messages from recognition thread
                    while recognition_thread.is_alive() or not self.result_queue.empty():
                        try:
                            msg = self.result_queue.get(timeout=1)
                            
                            if msg.startswith("Authenticated"):
                                parts = msg.split(": ")
                                if len(parts) >= 3:
                                    self.authenticated = True
                                    self.authenticated_user = parts[1]
                                    confidence = float(parts[2].strip('%')) / 100
                                    self.last_auth_time = time.time()
                                    status.success(
                                        f"✅ Authenticated as {self.authenticated_user} "
                                        f"(Confidence: {confidence:.2%})"
                                    )
                                    time.sleep(2)
                                    st.rerun()
                            
                            messages.append(msg)
                            log.markdown("\n".join(messages[-3:]))
                            
                        except queue.Empty:
                            time.sleep(0.1)
                        except Exception as e:
                            status.error(f"Error during authentication: {str(e)}")
                            break
                    
                    # Clean up
                    camera_placeholder.empty()
        
        return self.authenticated

# Initialize in session state
if 'face_auth' not in st.session_state:
    st.session_state.face_auth = FaceAuthenticator(
        "face_dataset"  # Changed to relative path
    )

PROTECTED_RESOURCES = {
    "Notepad": "notepad.exe",
    "WhatsApp": "whatsapp.exe",
    "Documents": os.path.expanduser("~/Documents"),
    "Project Files": os.path.expanduser("~/Desktop/mini proj")
}

# Rest of your code...
def execute_protected_action(resource_name):
    """Handle protected resource access with authentication"""
    if st.session_state.face_auth.authenticate():
        resource_path = PROTECTED_RESOURCES.get(resource_name)
        if resource_path:
            try:
                if resource_path.endswith(".exe"):
                    subprocess.Popen(resource_path)
                    st.success(f"✅ {resource_name} opened successfully!")
                else:
                    os.startfile(resource_path)
                    st.success(f"✅ {resource_name} accessed successfully!")
                return True
            except Exception as e:
                st.error(f"❌ Failed to open {resource_name}: {str(e)}")
        else:
            st.error("Invalid resource specified")
    return False

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

def home_interface():
    """Home screen with basic system operations"""
    st.header("System Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Commands")
        if st.button("Lock System"):
            ctypes.windll.user32.LockWorkStation()
            st.success("System locked!")
            
        if st.button("Shutdown"):
            os.system("shutdown /s /t 1")
            
        if st.button("Restart"):
            os.system("shutdown /r /t 1")
            
        if st.button("Sleep"):
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    
    with col2:
        st.subheader("System Info")
        st.write(f"OS: {platform.system()} {platform.release()}")
        st.write(f"Processor: {platform.processor()}")
        battery = psutil.sensors_battery()
        st.write(f"Battery: {battery.percent}% {'(Charging)' if battery.power_plugged else ''}")

def protected_resources_interface():
    """Interface for accessing protected resources"""
    st.header("🔒 Protected Resources")
    st.warning("These resources require face authentication to access")
    
    selected_resource = st.selectbox("Select a resource to access:", 
                                   list(PROTECTED_RESOURCES.keys()))
    
    if st.button(f"Access {selected_resource}"):
        if execute_protected_action(selected_resource):
            st.balloons()

def main_interface():
    """Main application interface"""
    st.title("🤖 AI Desktop Assistant")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose a mode:", 
                               ["Home", "OCR", "Calorie Tracker", "Chatbot", "Protected Resources"])
    
    if app_mode == "Home":
        home_interface()
    elif app_mode == "OCR":
        ocr_interface()
    elif app_mode == "Calorie Tracker":
        calorie_tracker_interface()
    elif app_mode == "Chatbot":
        chatbot_interface()
    elif app_mode == "Protected Resources":
        protected_resources_interface()

if __name__ == "__main__":
    main_interface()

