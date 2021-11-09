# tflite1.py

# Run a tensorflowlite object detector on an example video instead of the camera (better for testing)

import cv2
import imutils 
import time 
import config 
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions

rtsp = './examplevideos/example0.avi' # use an example video file now instead of the camera

windowName = "Video Window Resized"
cv2.namedWindow(windowName)
cv2.moveWindow(windowName, 850, 600)
cv2.setWindowProperty(windowName, cv2.WND_PROP_TOPMOST, 1)

model_path = 'ssd_mobilenet_v2_coco_quant_postprocess.tflite'

options = ObjectDetectorOptions(
    num_threads=2,
    score_threshold=0.7,
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

        # The detection time is 42ms and the time per frame at 15 fps is 67 ms therefore we need to wait here 67-42=25 ms
        # when the source is a video. Plus there is some other overhead so take off another 5 ms to give 20 ms. 
        # If it is the camera then we don't have to do this.
        # This is going to be dependent on the host processor.
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
