import streamlit as st
import threading
import queue
import time
import os
from facerecog_code import load_known_faces, recognize_faces

class FaceAuthenticator:
    def __init__(self, database_path):
        if not os.path.exists(database_path):
            raise FileNotFoundError(f"Database path not found: {database_path}")
            
        self.database_path = database_path
        self.result_queue = queue.Queue()
        self.authenticated = False
        self.authenticated_user = None
        self.auth_timeout = 1800  # 30 minutes
        self.min_confidence = 0.6
        self._recognition_thread = None

    def run_recognition(self):
        try:
            known_faces, known_names = load_known_faces(self.database_path)
            recognize_faces(known_faces, known_names, self.result_queue, self.min_confidence)
        except Exception as e:
            self.result_queue.put(f"Error: {str(e)}")

    def is_session_valid(self):
        return (self.authenticated and 
                (time.time() - self.last_auth_time) < self.auth_timeout)

    def authenticate(self):
        if self.is_session_valid():
            return True
            
        st.title("🔒 Face Authentication")
        with st.expander("Authentication Panel", expanded=True):
            if st.button("Start Face Recognition"):
                with st.spinner("Initializing camera..."):
                    self.authenticated = False
                    self._recognition_thread = threading.Thread(
                        target=self.run_recognition,
                        daemon=True
                    )
                    self._recognition_thread.start()
                    
                    status = st.empty()
                    while True:
                        try:
                            msg = self.result_queue.get(timeout=1)
                            if msg.startswith("Authenticated"):
                                parts = msg.split(": ")
                                self.authenticated = True
                                self.authenticated_user = parts[1].strip()
                                confidence = float(parts[2].strip('%'))
                                self.last_auth_time = time.time()
                                status.success(f"✅ Authenticated as {self.authenticated_user}")
                                time.sleep(2)
                                st.rerun()
                                break
                            status.info(msg)
                        except queue.Empty:
                            if not self._recognition_thread.is_alive():
                                break
        return self.authenticated
