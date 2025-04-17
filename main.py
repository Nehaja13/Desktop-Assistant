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

# Set page config MUST be the first Streamlit command and after imports

# Import all your existing modules
from ocr_exec import ocr_interface
from face_gui import FaceAuthenticator  # Changed from protect_resource
from calorie_tracker import calorie_tracker_interface
from chatbot import chatbot_interface

# Initialize face authenticator in session state
if 'face_auth' not in st.session_state:
    st.session_state.face_auth = FaceAuthenticator(
        "C:/Users/Jammula Nehaja/OneDrive/Desktop/mini proj/face_dataset"
    )

# Protected resources configuration
PROTECTED_RESOURCES = {
    "Notepad": "notepad.exe",
    "WhatsApp": "whatsapp.exe",
    "Documents": r"C:/Users/Jammula Nehaja/Documents",
    "Project Files": r"C:/Users/Jammula Nehaja/OneDrive/Desktop/mini proj"
}

def execute_protected_action(resource_name):
    """Handle protected resource access with authentication"""
    if st.session_state.face_auth.authenticate():
        resource_path = PROTECTED_RESOURCES.get(resource_name)
        if resource_path:
            try:
                if resource_path.endswith(".exe"):
                    subprocess.Popen(resource_path)
                    st.success(f"{resource_name} opened successfully!")
                else:
                    os.startfile(resource_path)
                    st.success(f"{resource_name} accessed successfully!")
                return True
            except Exception as e:
                st.error(f"Failed to open {resource_name}: {str(e)}")
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

def execute_system_command(command):
    """Execute basic system operations based on voice/text command"""
    command = command.lower()
    response = ""
    
    try:
        # File Manager Commands
        if any(cmd in command for cmd in ["open file manager", "open files", "show files"]):
            if os.name == 'nt':  # Windows
                os.startfile(os.environ['USERPROFILE'])
                response = "File manager opened"
            elif os.name == 'posix':  # Mac/Linux
                subprocess.run(['xdg-open', os.path.expanduser('~')])
                response = "File manager opened"
        
        # Browser Commands
        elif any(cmd in command for cmd in ["open browser", "open chrome", "open web browser"]):
            webbrowser.open('https://www.google.com')
            response = "Browser opened"
        
        # Terminal Commands
        elif any(cmd in command for cmd in ["open terminal", "open command prompt", "open cmd"]):
            if os.name == 'nt':  # Windows
                os.system('start cmd')
            elif os.name == 'posix':  # Mac/Linux
                subprocess.run(['gnome-terminal'])
            response = "Terminal opened"
        
        # Protected Resources - MODIFIED SECTION
        elif "open notepad" in command:
            if execute_protected_action("Notepad"):
                response = "Notepad opened successfully"
            else:
                response = "Notepad access denied"
        
        elif "open whatsapp" in command:
            if execute_protected_action("WhatsApp"):
                response = "WhatsApp opened successfully"
            else:
                response = "WhatsApp access denied"
        
        elif any(cmd in command for cmd in ["open documents", "my documents"]):
            if execute_protected_action("Documents"):
                response = "Documents opened successfully"
            else:
                response = "Documents access denied"
        
        elif "open project files" in command:
            if execute_protected_action("Project Files"):
                response = "Project files opened successfully"
            else:
                response = "Project files access denied"
        
        # New System Power Commands
        elif any(cmd in command for cmd in ["shutdown", "shut down", "turn off"]):
            if os.name == 'nt':
                os.system("shutdown /s /t 1")
                response = "System shutting down..."
            else:
                subprocess.run(['shutdown', '-h', 'now'])
                response = "System shutting down..."
        
        elif any(cmd in command for cmd in ["restart", "reboot"]):
            if os.name == 'nt':
                os.system("shutdown /r /t 1")
                response = "System restarting..."
            else:
                subprocess.run(['shutdown', '-r', 'now'])
                response = "System restarting..."
        
        elif any(cmd in command for cmd in ["sleep", "hibernate"]):
            if os.name == 'nt':
                ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
                response = "System going to sleep..."
            else:
                subprocess.run(['systemctl', 'suspend'])
                response = "System going to sleep..."
        
        elif any(cmd in command for cmd in ["lock screen", "lock computer"]):
            if os.name == 'nt':
                ctypes.windll.user32.LockWorkStation()
                response = "Screen locked"
            else:
                subprocess.run(['gnome-screensaver-command', '-l'])
                response = "Screen locked"
        
        elif "battery saver on" in command:
            if os.name == 'nt':
                # Windows battery saver (simplified approach)
                subprocess.run(['powercfg', '/setactive', 'SCHEME_CURRENT'])
                response = "Battery saver mode activated"
            else:
                # Linux power saving (simplified)
                subprocess.run(['gnome-power-statistics'])
                response = "Power saving features enabled"
        
        elif "battery status" in command or "battery level" in command:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = "plugged in" if battery.power_plugged else "not plugged in"
                response = f"Battery status: {percent}% ({plugged})"
            else:
                response = "Battery information not available"
        
        elif "system information" in command or "system info" in command:
            system_info = f"""
            System: {platform.system()} {platform.release()}
            Processor: {platform.processor()}
            Architecture: {platform.architecture()[0]}
            """
            if os.name == 'nt':
                info = subprocess.check_output('systeminfo', shell=True).decode('utf-8')
                response = f"System Information:\n{system_info}\n{info}"
            else:
                info = subprocess.check_output(['uname', '-a']).decode('utf-8')
                response = f"System Information:\n{system_info}\n{info}"
        
        # Rest of your existing commands...
        elif "take screenshot" in command or "capture screen" in command:
            screenshots_dir = os.path.join(os.path.expanduser("~"), "Desktop", "Assistant_Screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = os.path.join(screenshots_dir, f"screenshot_{timestamp}.png")
            
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            if os.path.exists(screenshot_path):
                response = f"Screenshot saved to: {screenshot_path}"
                if os.name == 'nt':
                    os.startfile(screenshot_path)
                elif os.name == 'posix':
                    subprocess.run(['xdg-open', screenshot_path])
            else:
                response = "Failed to save screenshot"
        
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
    st.title("My App")
    main()
