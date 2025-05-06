from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

model = YOLO("C:/Users/bryan/OneDrive/Documentos/Tesis/fall_detection/runs/detect/train7/weights/best.pt")
model_yolo = YOLO("yolo11n.pt")
camera = "https://192.168.1.91:8080/video"
link = "C:/Users/bryan/OneDrive/Documentos/Tesis/Dataset CAUCAFall/CAUCAFall/Subject.5/Fall sitting/FallSittingS5.avi"
cap = cv2.VideoCapture(link)
video_fps = cap.get(cv2.CAP_PROP_FPS)
frame_rate = 6
frame_step = int(video_fps // frame_rate)
frame_idx = 0

fall_counter = 0  # Contador de frames con caída
fall_threshold = 3  # Número de frames consecutivos necesarios

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    if frame_idx % frame_step == 0:
        results = model_yolo(frame, classes=[0], conf=0.5, device="cpu", stream=True)
        fall_detected_in_frame = False  # Bandera para este frame

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cropped = frame[y1:y2, x1:x2]

                if cropped.size == 0:
                    continue

                fall_res = model(cropped, classes=[1], conf=0.5, device="cpu", stream=True)
                fall_detected = any(r.boxes for r in fall_res)

                if fall_detected:
                    fall_detected_in_frame = True

                label = "FALL" if fall_detected else "Normal"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255) if fall_detected else (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (0, 0, 255) if fall_detected else (255, 255, 255), 2)

        # Actualizar contador de caídas consecutivas
        if fall_detected_in_frame:
            fall_counter += 1
        else:
            fall_counter = 0

        if fall_counter >= fall_threshold:
            print("-------------------- CAIDA DETECTADA -------------------- ")
            fall_counter = 0

        frame_idx = 0
        cv2.imshow("YOLO Inference", frame)
    frame_idx += 1


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()