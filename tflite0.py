# tflite0.py

# Run a tensorflowlite object detector on the camera image frames and show the detection time
# and print info about any objects detected. On the Raspberry Pi we see that the detection time
# is approximately 100 ms whereas the cycle time at 15 fps is 67 ms so we are running flat out
# when getting video data from a file and would be missing every second frame when running from 
# the camera.

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
cv2.moveWindow(windowName, 850, 600)
cv2.setWindowProperty(windowName, cv2.WND_PROP_TOPMOST, 1)

model_path = 'ssd_mobilenet_v1_1_metadata_1.tflite'
options = ObjectDetectorOptions(
    num_threads=2,
    score_threshold=0.6,
    max_results=3,
    enable_edgetpu=False)

detector = ObjectDetector(model_path=model_path, options=options)

def main():
    cap = cv2.VideoCapture(rtsp)

    showVideo = 1 

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
                break

        smallFrame = imutils.resize(frame, width=800) 

        st = time.time()
        detections = detector.detect(frame)
        et = time.time() - st
        print(et)
        if detections:
            print(detections)

        if showVideo:
            cv2.imshow('Video Window Resized', smallFrame) 

        k = cv2.waitKey(1) 
        
        if k & 0xFF == ord('q'):
            break
        elif k & 0xFF == ord('0'): 
            showVideo = 0
        elif k & 0xFF == ord('1'): 
            showVideo = 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
