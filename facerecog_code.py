# import os
# import cv2
# import face_recognition
# import numpy as np
# import dlib  # Import dlib for correlation tracking

# # Load known faces from the database
# def load_known_faces(database_path):
#     known_face_encodings = []
#     known_face_names = []

#     for person_name in os.listdir(database_path):
#         person_folder = os.path.join(database_path, person_name)
#         if os.path.isdir(person_folder):
#             for image_name in os.listdir(person_folder):
#                 image_path = os.path.join(person_folder, image_name)
#                 image = face_recognition.load_image_file(image_path)
#                 face_encoding = face_recognition.face_encodings(image)
#                 if len(face_encoding) > 0:  # Ensure at least one face is found
#                     known_face_encodings.append(face_encoding[0])
#                     known_face_names.append(person_name)

#     return known_face_encodings, known_face_names

# # Initialize webcam
# def recognize_faces(known_face_encodings, known_face_names):
#     video_capture = cv2.VideoCapture(0)

#     if not video_capture.isOpened():
#         print("Error: Could not open webcam.")
#         return

#     # Set the recognition threshold (adjust as needed)
#     recognition_threshold = 0.4  # Lower values are stricter

#     # Track recognized faces to limit responses
#     recognized_faces = set()
#     face_trackers = {}  # Dictionary to store face trackers
#     frame_counter = 0  # Counter to skip frames
#     cooldown_frames = 30  # Cooldown period for recognized faces

#     while True:
#         # Capture frame-by-frame
#         ret, frame = video_capture.read()
#         if not ret:
#             print("Error: Failed to capture frame.")
#             break

#         # Skip frames to reduce processing load
#         frame_counter += 1
#         if frame_counter % 3 != 0:  # Process every 3rd frame
#             continue

#         # Convert the image from BGR color (OpenCV) to RGB color (face_recognition)
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         # Update face trackers
#         faces_to_delete = []
#         for face_id, tracker in face_trackers.items():
#             tracking_quality = tracker.update(rgb_frame)
#             if tracking_quality < 7:  # If tracking quality is poor, mark for deletion
#                 faces_to_delete.append(face_id)

#         # Delete poor-quality trackers
#         for face_id in faces_to_delete:
#             del face_trackers[face_id]

#         # Detect new faces if no trackers are active
#         if not face_trackers:
#             face_locations = face_recognition.face_locations(rgb_frame)
#             face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#             for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#                 # Calculate face distances to known faces
#                 face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#                 best_match_index = np.argmin(face_distances)
#                 name = "Unknown"  # Default to "Unknown"

#                 # Check if the best match is within the threshold
#                 if face_distances[best_match_index] < recognition_threshold:
#                     name = known_face_names[best_match_index]
#                     confidence = 1 - face_distances[best_match_index]
#                     if name not in recognized_faces:
#                         print(f"Recognized: {name} with confidence: {confidence:.2f}")
#                         recognized_faces.add(name)
#                         # Start tracking the face
#                         tracker = dlib.correlation_tracker()
#                         rect = dlib.rectangle(left, top, right, bottom)  # Use dlib.rectangle
#                         tracker.start_track(rgb_frame, rect)
#                         face_trackers[name] = tracker
#                 else:
#                     print("Unknown face detected")

#                 # Draw a rectangle around the face
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

#                 # Draw the name and confidence below the face
#                 label = f"{name} ({confidence:.2f})" if name != "Unknown" else "Unknown"
#                 cv2.putText(frame, label, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

#         # Display the resulting image
#         cv2.imshow('Video', frame)

#         # Break the loop if 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Release the webcam and close windows
#     video_capture.release()
#     cv2.destroyAllWindows()

# # Main function
# if __name__ == "__main__":
#     database_path = "C:/Users/Jammula Nehaja/OneDrive/Desktop/mini proj/face_dataset"
#     known_face_encodings, known_face_names = load_known_faces(database_path)
#     recognize_faces(known_face_encodings, known_face_names)













#pip install streamlit opencv-python face_recognition dlib numpy
# face_recognition_core.py
# import os
# import cv2
# import face_recognition
# import numpy as np
# import dlib

# def load_known_faces(database_path):
#     known_face_encodings = []
#     known_face_names = []
#     for person_name in os.listdir(database_path):
#         person_folder = os.path.join(database_path, person_name)
#         if os.path.isdir(person_folder):
#             for image_name in os.listdir(person_folder):
#                 image_path = os.path.join(person_folder, image_name)
#                 image = face_recognition.load_image_file(image_path)
#                 face_encoding = face_recognition.face_encodings(image)
#                 if len(face_encoding) > 0:
#                     known_face_encodings.append(face_encoding[0])
#                     known_face_names.append(person_name)
#     return known_face_encodings, known_face_names

# def recognize_faces(known_face_encodings, known_face_names):
#     video_capture = cv2.VideoCapture(0)

#     if not video_capture.isOpened():
#         print("Error: Could not open webcam.")
#         return

#     recognition_threshold = 0.4
#     recognized_faces = set()
#     face_trackers = {}
#     frame_counter = 0
#     cooldown_frames = 30

#     while True:
#         ret, frame = video_capture.read()
#         if not ret:
#             print("Error: Failed to capture frame.")
#             break

#         frame_counter += 1
#         if frame_counter % 3 != 0:
#             continue

#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         faces_to_delete = []
#         for face_id, tracker in face_trackers.items():
#             tracking_quality = tracker.update(rgb_frame)
#             if tracking_quality < 7:
#                 faces_to_delete.append(face_id)
#         for face_id in faces_to_delete:
#             del face_trackers[face_id]

#         if not face_trackers:
#             face_locations = face_recognition.face_locations(rgb_frame)
#             face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#             for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#                 face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#                 best_match_index = np.argmin(face_distances)
#                 name = "Unknown"

#                 if face_distances[best_match_index] < recognition_threshold:
#                     name = known_face_names[best_match_index]
#                     confidence = 1 - face_distances[best_match_index]
#                     if name not in recognized_faces:
#                         print(f"Recognized: {name} with confidence: {confidence:.2f}")
#                         recognized_faces.add(name)
#                         tracker = dlib.correlation_tracker()
#                         rect = dlib.rectangle(left, top, right, bottom)
#                         tracker.start_track(rgb_frame, rect)
#                         face_trackers[name] = tracker
#                 else:
#                     print("Unknown face detected")

#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
#                 label = f"{name} ({confidence:.2f})" if name != "Unknown" else "Unknown"
#                 cv2.putText(frame, label, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

#         cv2.imshow('Video', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     video_capture.release()
#     cv2.destroyAllWindows()






# face_recognition_core.py

import os
import cv2
import face_recognition
import numpy as np
import dlib

def load_known_faces(database_path):
    known_face_encodings = []
    known_face_names = []
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
    return known_face_encodings, known_face_names

def recognize_faces(known_face_encodings, known_face_names, result_queue=None):
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        if result_queue:
            result_queue.put("Error: Could not open webcam.")
        else:
            print("Error: Could not open webcam.")
        return

    recognition_threshold = 0.4
    recognized_faces = set()
    face_trackers = {}
    frame_counter = 0
    cooldown_frames = 30

    while True:
        ret, frame = video_capture.read()
        if not ret:
            if result_queue:
                result_queue.put("Error: Failed to capture frame.")
            else:
                print("Error: Failed to capture frame.")
            break

        frame_counter += 1
        if frame_counter % 3 != 0:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces_to_delete = []
        for face_id, tracker in face_trackers.items():
            tracking_quality = tracker.update(rgb_frame)
            if tracking_quality < 7:
                faces_to_delete.append(face_id)
        for face_id in faces_to_delete:
            del face_trackers[face_id]

        if not face_trackers:
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                name = "Unknown"

                if face_distances[best_match_index] < recognition_threshold:
                    name = known_face_names[best_match_index]
                    confidence = 1 - face_distances[best_match_index]
                    if name not in recognized_faces:
                        msg = f"Recognized: {name} with confidence: {confidence:.2f}"
                        recognized_faces.add(name)
                        if result_queue:
                            result_queue.put(msg)
                        else:
                            print(msg)
                        tracker = dlib.correlation_tracker()
                        rect = dlib.rectangle(left, top, right, bottom)
                        tracker.start_track(rgb_frame, rect)
                        face_trackers[name] = tracker
                else:
                    if result_queue:
                        result_queue.put("Unknown face detected")
                    else:
                        print("Unknown face detected")

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                label = f"{name} ({confidence:.2f})" if name != "Unknown" else "Unknown"
                cv2.putText(frame, label, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
