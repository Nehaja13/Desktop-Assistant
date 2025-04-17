
import face_recognition
import cv2
import os
import numpy as np

def load_known_faces(dataset_path):
    known_encodings = []
    known_names = []
    
    for name in os.listdir(dataset_path):
        person_dir = os.path.join(dataset_path, name)
        if os.path.isdir(person_dir):
            for img_file in [f for f in os.listdir(person_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]:
                img_path = os.path.join(person_dir, img_file)
                try:
                    img = face_recognition.load_image_file(img_path)
                    encodings = face_recognition.face_encodings(img)
                    if encodings:
                        known_encodings.append(encodings[0])
                        known_names.append(name)
                except Exception as e:
                    print(f"Skipping {img_path}: {str(e)}")
    
    return known_encodings, known_names

def recognize_faces(known_encodings, known_names, result_queue, min_confidence=0.6):
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        result_queue.put("Error: Could not access camera")
        return

    try:
        while True:
            ret, frame = video.read()
            if not ret:
                continue

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_frame = small_frame[:, :, ::-1]

            face_locs = face_recognition.face_locations(rgb_frame)
            face_encs = face_recognition.face_encodings(rgb_frame, face_locs)

            for face_encoding in face_encs:
                matches = face_recognition.compare_faces(known_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_idx = np.argmin(face_distances)

                if matches[best_match_idx]:
                    confidence = 1 - face_distances[best_match_idx]
                    if confidence >= min_confidence:
                        name = known_names[best_match_idx]
                        result_queue.put(f"Authenticated:{name}:{confidence*100:.1f}%")
                        video.release()
                        return

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        video.release()
        cv2.destroyAllWindows()
