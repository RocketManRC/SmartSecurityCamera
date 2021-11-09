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
cv2.moveWindow(windowName, 850, 600)
cv2.setWindowProperty(windowName, cv2.WND_PROP_TOPMOST, 1)

model_path = 'ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite'

options = ObjectDetectorOptions(
    num_threads=2,
    score_threshold=0.7,
    max_results=3,
    enable_edgetpu=True)

detector = ObjectDetector(model_path=model_path, options=options)

def main():
    cap = cv2.VideoCapture(rtsp)

    showVideo = 1 

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
                break

        detections = detector.detect(frame)

        if detections:
            annotatedFrame = utils.visualize(frame, detections) # use the visualize utility to show the objects
            smallFrame = imutils.resize(annotatedFrame, width=800) 
        else:
            smallFrame = imutils.resize(frame, width=800)

        if showVideo:
            cv2.imshow('Video Window Resized', smallFrame) 

        k = cv2.waitKey(20) 
        
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
