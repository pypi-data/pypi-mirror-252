import cv2
from standup_face_recognition2.MTCNN_detector import MTCNN_detector
from standup_face_recognition2.face_recognition import Siamese
from standup_face_recognition2.utils import imread_templates, resize_images_tensor, show_face, standup_roulette
from standup_face_recognition2.pedestrian_detector import PedestrianDetector


def main():
    # template_dict = imread_templates('/home/timo/pip_installable/Webcam/faces_from_webcam')
    names = ['Timo', 'Nitin', 'Karl', 'Martin', 'Kai', 'Robert', 'Hiep', 'Matthias', 'Bharat']
    order_person = ['Timo', 'Bharat', 'Martin', 'Matthias', 'Kai', 'Robert', 'Nitin', 'Hiep', 'Karl']
    person, direction = standup_roulette(names)
    # face recognition
    face_recognition = Siamese()
    # Open a connection to the webcam (0 represents the default camera)
    cap = cv2.VideoCapture(0)
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('/home/timo/face_recognition/output.mp4', fourcc, 20.0, (640, 480))

    # Check if the webcam opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    # image = cv2.imread('/home/timo/pip_installable/Webcam/2024-01-16-124613.jpg')
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Person detection
    pedestrian_detector = PedestrianDetector()
    # MTCNN face detector
    mtcnn_face_detector = MTCNN_detector()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # frame = image

        # Check if the frame was successfully captured
        if not ret:
            print("Error: Could not read frame.")
            break

        detected_ped_boxes, detected_labels, cropped_ped_images = pedestrian_detector.detect_pedestrians(frame)
        # pedestrian_detector.visualize_pedestrian_detection(frame, detected_ped_boxes, detected_labels,
        #                                                   '/home/timo/pip_installable/Webcam/temp')

        detected_faces_mtcnn = mtcnn_face_detector.get_bbox_detection(cropped_ped_images)
        # mtcnn_face_detector.visualize_face_detection(frame, detected_faces_mtcnn, detected_ped_boxes,
        #                                             '/home/timo/pip_installable/Webcam/temp')

        detected_faces_mtcnn_resized = []
        for ped_box in detected_faces_mtcnn:
            if ped_box[0][0] is not None:
                resized_faces = resize_images_tensor(ped_box, 128)
                face_det_reg = face_recognition.face_recognition(resized_faces, names)
                detected_faces_mtcnn_resized.append(face_det_reg)
            else:
                continue

        show_face(frame, detected_faces_mtcnn_resized, detected_ped_boxes, person, direction)

        if cv2.waitKey(1) & 0xFF == ord('n'):
            person_ind = order_person.index(person)
            if direction is 'clockwise':
                person = order_person[(person_ind + 1) % len(order_person)]
            else:
                person = order_person[(person_ind - 1) % len(order_person)]

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    # out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
