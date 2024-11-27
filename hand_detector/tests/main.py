import pickle
import cv2
import mediapipe as mp
import numpy as np


model_dict = pickle.load(open(r'../train_classifier/model.p', 'rb'))
model = model_dict['model']


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.6)


labels_dict = {
    -1:"Nan",
    0:"B",
    1:"A",
    2:"C",
    3:"D",
    4:"E",
}

cap = cv2.VideoCapture('../collect_images/images/0/0.jpg')

# cap = cv2.VideoCapture(0)
while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

            try:
                prediction = model.predict([np.asarray(data_aux)])
                print(prediction)
            except:
                prediction = [-1]
            predicted_character = labels_dict[int(prediction[0])]
            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10
            x_, y_, data_aux = [], [], []
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                        cv2.LINE_AA)

        # x1 = int(min(x_) * W) - 10
        # y1 = int(min(y_) * H) - 10
        #
        # x2 = int(max(x_) * W) - 10
        # y2 = int(max(y_) * H) - 10

        # try:
        #     prediction = model.predict([np.asarray(data_aux)])
        # except:
        #     prediction = [-1]
        # predicted_character = labels_dict[int(prediction[0])]
        #
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        # cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
        #             cv2.LINE_AA)
    cv2.imshow('So`zlar', frame)
    cv2.waitKey(1)


cap.release()
cv2.destroyAllWindows()