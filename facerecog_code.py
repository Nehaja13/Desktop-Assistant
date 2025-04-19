import os
import cv2
import face_recognition
import numpy as np
import dlib

def load_known_faces(database_path):
    known_face_encodings = []
    known_face_names = []
    try:
        for person_name in os.listdir(database_path):
            person_folder = os.path.join(database_path, person_name)
            if os.path.isdir(person_folder):
                for image_name in os.listdir(person_folder):
                    image_path = os.path.join(person_folder, image_name)
                    image = face_recognition.load_image_file(image_path)
                    face_encoding = face_recognition.face_encodings(image)
                    if len(face_encoding) > 0:
                        known_face_encodings.append(face_encoding[0])
                        known_face_names.append(person_name)
    except Exception as e:
        print(f"Error loading known faces: {e}")
    return known_face_encodings, known_face_names

def is_real_face(frame, face_location):
    """Enhanced anti-spoofing checks"""
    try:
        (top, right, bottom, left) = face_location
        face_roi = frame[top:bottom, left:right]
        
        if face_roi.size == 0:
            return False
        
        # 1. Laplacian variance for blur detection
        gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # 2. Color diversity check
        hsv = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)
        color_std = np.std(hsv[:,:,0])
        
        # Thresholds
        if variance < 100 or color_std < 15:
            return False
            
        return True
    except:
        return False

def recognize_faces(known_face_encodings, known_face_names, result_queue=None):
    try:
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            if result_queue:
                result_queue.put("Error: Could not open webcam.")
            return

        recognition_threshold = 0.6
        required_real_frames = 5
        real_frame_count = 0
        frame_counter = 0
        authenticated = False

        while True:
            ret, frame = video_capture.read()
            if not ret:
                if result_queue:
                    result_queue.put("Error: Failed to capture frame.")
                break

            frame_counter += 1
            if frame_counter % 2 != 0:
                continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            current_name = "Unknown"
            current_confidence = 0.0
            is_real = False

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                is_real = is_real_face(frame, (top, right, bottom, left))
                
                if is_real:
                    real_frame_count += 1
                else:
                    real_frame_count = 0
                    if result_queue:
                        result_queue.put("Suspicious: Possible photo detected")
                    continue

                if real_frame_count < required_real_frames:
                    continue

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                current_confidence = 1 - face_distances[best_match_index]

                if face_distances[best_match_index] < recognition_threshold:
                    current_name = known_face_names[best_match_index]
                    if result_queue:
                        result_queue.put(f"Authenticated: {current_name} with confidence: {current_confidence:.2f}")
                    authenticated = True
                    break

                # Visualization
                color = (0, 255, 0) if is_real else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                label = f"{current_name} ({current_confidence:.2f})" if current_name != "Unknown" else "Unknown"
                cv2.putText(frame, label, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                cv2.putText(frame, "REAL" if is_real else "PHOTO", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            if authenticated:
                break

            cv2.imshow('Face Authentication', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        if result_queue:
            result_queue.put(f"Error: {str(e)}")
    finally:
        video_capture.release()
        cv2.destroyAllWindows()

