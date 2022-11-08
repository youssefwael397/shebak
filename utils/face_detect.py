import face_recognition
import os
import glob
import cv2

def get_faces_paths_and_names(images_path):
    names = []
    faces_paths = []

    for name in os.listdir(images_path):
        images_mask = '%s%s/*.jpg' % (images_path, name)
        images_paths = glob.glob(images_mask)
        faces_paths += images_mask
        names += [name for x in images_paths]

    return names, faces_paths


def get_face_encoding(img_path):
    image = face_recognition.load_image_file(img_path)
    face_encodings = face_recognition.face_encodings(image)
    return face_encodings[0]


def get_faces(faces_paths):
    faces = [get_face_encoding(img_path) for img_path in faces_paths]
    return faces


def open_face_detect_cam(faces, names):
    vc = cv2.VideoCapture(0)

    while True:
        ret, frame = vc.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(frame_rgb)

        for face in faces:
            top, right, bottom, left = face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            encoding = face_recognition.face_encodings(frame_rgb, [face])[0]

            results = face_recognition.compare_faces(faces, encoding)
            if any(results):
                name = names[results.index(True)]
            else:
                name = 'Unknown'

            cv2.putText(frame_rgb, name, (left, bottom + 25),
                        cv2.FONT_HERSHEY_PLAIN, (255, 0, 0), 2,)

        cv2.imshow('win', frame)
        k = cv2.waitKey(1)
        if ord('q') == k:
            break

    # close the video capture
    cv2.destroyAllWindows()
    vc.release()
