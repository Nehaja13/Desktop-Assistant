import streamlit as st
import threading
import os
import subprocess
import queue
import time
import cv2
import numpy as np
from facerecog_code import load_known_faces, recognize_faces

class FaceAuthenticator:
    def __init__(self, database_path):
        self.database_path = database_path
        self.result_queue = queue.Queue()
        self.authenticated = False
        self.authenticated_user = None
        self.auth_timeout = 1800  # 30 minutes in seconds
        self.last_auth_time = 0
        self.min_confidence = 0.6  # Minimum confidence threshold
        self.camera_active = False

    def run_recognition(self):
        """Run face recognition in a separate thread"""
        try:
            known_face_encodings, known_face_names = load_known_faces(self.database_path)
            self.camera_active = True
            recognize_faces(known_face_encodings, known_face_names, self.result_queue, self.min_confidence)
        except Exception as e:
            self.result_queue.put(f"Error: {str(e)}")
        finally:
            self.camera_active = False

    def is_session_valid(self):
        """Check if the authentication session is still valid"""
        current_time = time.time()
        return (self.authenticated and 
                current_time - self.last_auth_time < self.auth_timeout)

    def reset_authentication(self):
        """Reset authentication status"""
        self.authenticated = False
        self.authenticated_user = None
        self.last_auth_time = 0

    def authenticate(self):
        """Handle the authentication flow with Streamlit UI"""
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


def protect_resource(resource_name, resource_path):
    """
    Wrapper function to protect resources with face authentication
    (Can be moved to main.py if preferred)
    """
    auth = FaceAuthenticator("face_dataset")  # Relative path
    
    if not auth.authenticate():
        st.warning("Authentication failed or was cancelled")
        st.stop()
    
    try:
        if resource_path.endswith(".exe"):
            subprocess.Popen(resource_path)
            st.success(f"✅ {resource_name} launched successfully!")
        else:
            os.startfile(resource_path)
            st.success(f"✅ {resource_name} accessed successfully!")
    except Exception as e:
        st.error(f"❌ Failed to access {resource_name}: {str(e)}")
