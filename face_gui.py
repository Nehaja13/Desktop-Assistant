import streamlit as st
import threading
import queue
import time
import os
import subprocess
from facerecog_code import load_known_faces, recognize_faces

class FaceAuthenticator:
    def __init__(self, database_path):
        self.database_path = database_path
        self.result_queue = queue.Queue()
        self.authenticated = False
        self.authenticated_user = None
        self.auth_timeout = 1800  # 30 minutes in seconds
        self.last_auth_time = 0

    def run_recognition(self):
        known_face_encodings, known_face_names = load_known_faces(self.database_path)
        recognize_faces(known_face_encodings, known_face_names, self.result_queue)

    def is_session_valid(self):
        return (self.authenticated and 
                time.time() - self.last_auth_time < self.auth_timeout)

    def authenticate(self):
        if self.is_session_valid():
            return True
            
        st.title("🔒 Face Authentication Required")
        with st.expander("Authentication Panel", expanded=True):
            st.write("Please authenticate using facial recognition to continue")
            
            if st.button("Start Face Recognition"):
                with st.spinner("Initializing camera..."):
                    recognition_thread = threading.Thread(target=self.run_recognition, daemon=True)
                    recognition_thread.start()
                    
                    status = st.empty()
                    log = st.empty()
                    messages = []
                    
                    while recognition_thread.is_alive():
                        try:
                            msg = self.result_queue.get(timeout=1)
                            if "Authenticated" in msg:
                                self.authenticated = True
                                self.authenticated_user = msg.split(": ")[1]
                                self.last_auth_time = time.time()
                                status.success(f"✅ Authenticated as {self.authenticated_user}")
                                time.sleep(2)
                                st.rerun()
                            messages.append(msg)
                            log.markdown("\n".join(messages[-3:]))
                        except queue.Empty:
                            time.sleep(0.1)
                    
        return False

def protect_resource(resource_name, resource_path):
    auth = FaceAuthenticator("C:/Users/Jammula Nehaja/OneDrive/Desktop/mini proj/face_dataset")
    
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

