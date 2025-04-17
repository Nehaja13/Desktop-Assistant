import streamlit as st
import threading
import queue
import time
from facerecog_code import load_known_faces, recognize_faces

class FaceAuthenticator:
    def __init__(self, database_path):
        self.database_path = database_path
        self.result_queue = queue.Queue()
        self.authenticated = False
        self.authenticated_user = None
        self.auth_timeout = 1800  # 30 minutes in seconds
        self.last_auth_time = 0
        self.min_confidence = 0.6
        self.camera_active = False

    def run_recognition(self):
        """Run face recognition in a separate thread"""
        known_face_encodings, known_face_names = load_known_faces(self.database_path)
        self.camera_active = True
        recognize_faces(known_face_encodings, known_face_names, self.result_queue, self.min_confidence)
        self.camera_active = False

    def is_session_valid(self):
        """Check if authentication session is still valid"""
        return (self.authenticated and 
                time.time() - self.last_auth_time < self.auth_timeout)

    def reset_authentication(self):
        """Reset authentication status"""
        self.authenticated = False
        self.authenticated_user = None
        self.last_auth_time = 0

    def authenticate(self):
        """Handle the authentication flow"""
        if self.is_session_valid():
            return True
            
        st.title("🔒 Face Authentication Required")
        with st.expander("Authentication Panel", expanded=True):
            st.write("Please authenticate using facial recognition to continue")
            
            if st.button("Start Face Recognition"):
                with st.spinner("Initializing camera..."):
                    self.reset_authentication()
                    recognition_thread = threading.Thread(target=self.run_recognition, daemon=True)
                    recognition_thread.start()
                    
                    status = st.empty()
                    log = st.empty()
                    messages = []
                    
                    while recognition_thread.is_alive() or not self.result_queue.empty():
                        try:
                            msg = self.result_queue.get(timeout=1)
                            if "Authenticated" in msg:
                                parts = msg.split(": ")
                                if len(parts) >= 3:
                                    self.authenticated = True
                                    self.authenticated_user = parts[1]
                                    confidence = float(parts[2].strip('%')) / 100
                                    self.last_auth_time = time.time()
                                    status.success(f"✅ Authenticated as {self.authenticated_user} (Confidence: {confidence:.2%})")
                                    time.sleep(2)
                                    st.rerun()
                            messages.append(msg)
                            log.markdown("\n".join(messages[-3:]))
                        except queue.Empty:
                            time.sleep(0.1)
        
        return self.authenticated
