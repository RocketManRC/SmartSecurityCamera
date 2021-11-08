# tflite3.py

# Back to the video camera again to test with processing every third frame

import cv2
import imutils 
import time 
import config 
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils 

rtsp = config.geturl() 

windowName = "Video Window Resized"
cv2.namedWindow(windowName)
cv2.moveWindow(windowName, 850, 600)
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

    showVideo = 1 
    frameCount = 0 

    while cap.isOpened():
        frameCount = frameCount + 1

        if frameCount % 3 == 0: 
            ret, frame = cap.read()

            if not ret:
                    break

            detections = detector.detect(frame)

            if detections:
                annotatedFrame = utils.visualize(frame, detections) 
                smallFrame = imutils.resize(annotatedFrame, width=800) 
            else:
                smallFrame = imutils.resize(frame, width=800)

            if showVideo:
                cv2.imshow('Video Window Resized', smallFrame) 
        else:
            cap.grab() 
            # can add other processing here...

        k = cv2.waitKey(1) # we don't need to wait when using the camera
        
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
