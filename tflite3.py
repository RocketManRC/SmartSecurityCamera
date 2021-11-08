# tflite3.py

# Lets solve the processing problem on the RasPi by only processing every second frame

import cv2
import imutils 
import time 
import config 
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils 

rtsp = './examplevideos/example0.avi' 

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
    frameCount = 0 # add a frameCount so we can only process every second frame (only odd numbered frames)

    while cap.isOpened():
        frameCount = frameCount + 1

        if frameCount & 1: # is it an odd numbered frame?
            ret, frame = cap.read()
        else:
            cap.grab() # no point in decoding it if we aren't going to use it
            continue

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

        if frameCount & 1: # is it an odd numbered frame?
            k = cv2.waitKey(67) # wait the full frame time of 67 ms
        else:
            k = cv2.waitKey(20) # else just add to the processing time
        
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
