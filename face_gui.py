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
        self.auth_timeout = 1800
        self.last_auth_time = 0
        self.spoof_attempts = 0
        self.max_spoof_attempts = 3

    def run_recognition(self):
        try:
            known_face_encodings, known_face_names = load_known_faces(self.database_path)
            recognize_faces(known_face_encodings, known_face_names, self.result_queue)
        except Exception as e:
            self.result_queue.put(f"Error: {str(e)}")

    def is_session_valid(self):
        return (self.authenticated and 
                time.time() - self.last_auth_time < self.auth_timeout)

    def authenticate(self):
        if self.is_session_valid():
            return True
            
        st.title("🔒 Face Authentication Required")
        st.warning("For security, please ensure you're physically present - photos will be detected")
        
        if st.button("Start Face Recognition"):
            with st.spinner("Initializing camera with anti-spoofing..."):
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
                            self.authenticated_user = msg.split(": ")[1].split(" with")[0]
                            self.last_auth_time = time.time()
                            status.success(f"✅ Authenticated as {self.authenticated_user}")
                            time.sleep(2)
                            st.rerun()
                        elif "Suspicious" in msg:
                            self.spoof_attempts += 1
                            if self.spoof_attempts >= self.max_spoof_attempts:
                                status.error("🚨 Multiple spoofing attempts detected. Access blocked.")
                                time.sleep(5)
                                st.stop()
                            status.warning("⚠️ Possible spoofing attempt detected. Please try again with your actual face.")
                        messages.append(msg)
                        log.markdown("\n".join(messages[-3:]))
                    except queue.Empty:
                        continue
                
        return False

def main():
    st.set_page_config(page_title="Secure Access", page_icon="🔒")
    auth = FaceAuthenticator("face_dataset")  # Update path to your dataset
    
    st.header("Protected Resource Access")
    
    if not auth.authenticate():
        st.warning("Please authenticate to continue")
        st.stop()
    
    st.success(f"Welcome, {auth.authenticated_user}!")
    
    resource_options = {
        "Notepad": "notepad.exe",
        "Calculator": "calc.exe",
        # Add more resources as needed
    }
    
    selected_resource = st.selectbox("Select a resource to access:", list(resource_options.keys()))
    
    if st.button("Access Resource"):
        try:
            if resource_options[selected_resource].endswith(".exe"):
                subprocess.Popen(resource_options[selected_resource])
                st.success(f"✅ {selected_resource} launched successfully!")
            else:
                os.startfile(resource_options[selected_resource])
                st.success(f"✅ {selected_resource} accessed successfully!")
        except Exception as e:
            st.error(f"❌ Failed to access {selected_resource}: {str(e)}")

if __name__ == "__main__":
    main()

