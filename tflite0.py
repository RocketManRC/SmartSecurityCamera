# tflite0.py

# Run a tensorflowlite object detector on the image frames and show the detection time
# and print info about any objects detected

import cv2
import imutils 
import time 
import config 
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions

rtsp = config.geturl() 

# Open the video window and place it somewhere convenient
windowName = "Video Window Resized"
cv2.namedWindow(windowName)
cv2.moveWindow(windowName, 1600, 600)
cv2.setWindowProperty(windowName, cv2.WND_PROP_TOPMOST, 1)

model_path = 'ssd_mobilenet_v1_1_metadata_1.tflite'
options = ObjectDetectorOptions(
    num_threads=2,
    score_threshold=0.5,
    max_results=3,
    enable_edgetpu=False)
detector = ObjectDetector(model_path=model_path, options=options)

def main():
    cap = cv2.VideoCapture(rtsp)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
                break

        smallFrame = imutils.resize(frame, width=640) 

        st = time.time()
        detections = detector.detect(frame)
        et = time.time() - st
        print(et)
        if detections:
            print(detections)

        cv2.imshow('Video Window Resized', smallFrame) 

        k = cv2.waitKey(1) 
        
        if k & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
