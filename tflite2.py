# tflite2.py

# Draw boxes around the detected objects in the example video

import cv2
import imutils 
import time 
import config 
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils # utils.py contains the code to draw the bounding boxes

rtsp = './examplevideos/example0.avi' 

windowName = "Video Window Resized"
cv2.namedWindow(windowName)
cv2.moveWindow(windowName, 1600, 400)
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

        detections = detector.detect(frame)

        if detections:
            annotatedFrame = utils.visualize(frame, detections) # use the visualize utility to show the objects
            smallFrame = imutils.resize(annotatedFrame, width=640) 
        else:
            smallFrame = imutils.resize(frame, width=640)

        cv2.imshow('Video Window Resized', smallFrame) 

        k = cv2.waitKey(41) 
        
        if k & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
