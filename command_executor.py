import os
import subprocess
import pyautogui
from datetime import datetime
from config import PROTECTED_RESOURCES, SCREENSHOTS_DIR

class CommandExecutor:
    @staticmethod
    def execute_protected_action(face_auth, resource_name):
        """Handle protected resource access with authentication"""
        if not face_auth.authenticate():
            return False, "Authentication failed"
            
        resource_path = PROTECTED_RESOURCES.get(resource_name)
        if not resource_path:
            return False, "Invalid resource specified"
            
        try:
            if resource_path.endswith(".exe"):
                subprocess.Popen(resource_path)
            else:
                os.startfile(resource_path)
            return True, f"{resource_name} opened successfully!"
        except Exception as e:
            return False, f"Failed to open {resource_name}: {str(e)}"

    @staticmethod
    def take_screenshot():
        """Capture and save screenshot"""
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(SCREENSHOTS_DIR, f"screenshot_{timestamp}.png")
        
        try:
            pyautogui.screenshot(screenshot_path)
            if os.path.exists(screenshot_path):
                return True, screenshot_path
            return False, "Failed to save screenshot"
        except Exception as e:
            return False, f"Screenshot error: {str(e)}"