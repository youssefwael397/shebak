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
        faces_paths += images_paths
        names += [name for x in images_paths]

    return names, faces_paths


def get_face_encodings(img_path):
    image = face_recognition.load_image_file(img_path)
    encoding = face_recognition.face_encodings(image)
    # print("encoding: " , encoding)
    return encoding[0]


def get_faces(faces_paths):
    # faces = []
    faces = [get_face_encodings(img_path) for img_path in faces_paths]
    return faces


def open_cam():
    vc = cv2.VideoCapture(0)

    while True:
        ret, frame = vc.read()
        if not ret:
            break
        cv2.imshow('video stream', frame)
        k = cv2.waitKey(1)
        if ord('q') == k:
            break

    # close the video capture
    cv2.destroyAllWindows()
    vc.release()


def open_face_detect_cam(faces, names):
    vc = cv2.VideoCapture("elharam.mp4")

    while True:
        ret, frame = vc.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detected_faces = face_recognition.face_locations(frame_rgb)

        for detected_face in detected_faces:
            top, right, bottom, left = detected_face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            encoding = face_recognition.face_encodings(
                frame_rgb, [detected_face])[0]

            results = face_recognition.compare_faces(faces, encoding)
            # print(faces)
            print(results)
            # print(names)

            # if any(results):
            if results[-1] == True:
                name=names[-1]
            elif any(results):
                name = names[results.index(True)]
            else:
                name = 'Unknown'

            # print("name: ", name)

            cv2.putText(frame, name, (left, bottom + 25),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv2.imshow('video stream', frame)
        k = cv2.waitKey(1)
        if ord('q') == k:
            break

    # close the video capture
    cv2.destroyAllWindows()
    vc.release()


def extract_and_save_faces(name, video_path):
    dir_path = f'images/registered/{name}'
    os.mkdir(dir_path)

    vc = cv2.VideoCapture(video_path)

    count = 0
    while (vc.isOpened()):
        ret, frame = vc.read()

        if not ret or count==21:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detected_faces = face_recognition.face_locations(frame_rgb)

        if len(detected_faces):
            cv2.imwrite(f'{dir_path}/{count}.jpg', frame)
            count += 1


    # close the video capture
    cv2.destroyAllWindows()
    vc.release()
