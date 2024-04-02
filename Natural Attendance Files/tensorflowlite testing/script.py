import cv2
import face_recognition

# Load the known faces and their labels
known_faces = []
known_labels = ["Karan", "Anmol"]

for label in known_labels:
    face_descriptors = []
    for i in range(1, 7):
        image_path = f"./Labels/{label}/{i}.jpg"
        image = face_recognition.load_image_file(image_path)
        face_descriptor = face_recognition.face_encodings(image)[0]
        face_descriptors.append(face_descriptor)
    known_faces.append(face_descriptors)

# Open the webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = video_capture.read()

    # Convert the frame to RGB
    rgb_frame = frame[:, :, ::-1]

    # Find all face locations and face encodings in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        # Compare the face encoding with the known faces
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = int(face_distances.argmin())

        if matches[best_match_index]:
            label = known_labels[best_match_index]
            # Draw a rectangle and label on the frame
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
video_capture.release()
cv2.destroyAllWindows()
