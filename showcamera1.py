# showcamera1.py

# Add some basic functions to work with the video (resize and annotate)
# and also measure the frame rate from the camera. Note that some cameras change the
# frame rate when they switch to night mode but I just use the result for the daylight
# mode to set the frame rate for the saved file (next step).

import cv2
import imutils # some handy add-ons to work with OpenCV
import config 
import time # added this to calculate the frame rate

rtsp = config.geturl() 

windowName = "Video Window Resized"
cv2.namedWindow(windowName)
cv2.moveWindow(windowName, 850, 600)
cv2.setWindowProperty(windowName, cv2.WND_PROP_TOPMOST, 1)

def main():
    cap = cv2.VideoCapture(rtsp)

    lastFrameCountTime = time.time()
    frameCount = 0
    
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
                break

        frameCount = frameCount + 1 # use this to calculate the framerate over 30 frames
        frameTime = time.time()

        if frameCount >= 30:
            frameCount = 0
            elapsedTime = frameTime - lastFrameCountTime
            lastFrameCountTime = frameTime
            fps = 30.0 / elapsedTime # this is the framerate over the last 30 frames
            print('fps: ', fps)
        
        smallFrame = imutils.resize(frame, width=800) # resize the frame with width 480

        cv2.rectangle(smallFrame, (100, 100), (200, 200), (0, 255, 0), 2) # draw a red rectangle as an example of annotation
        cv2.putText(smallFrame, 'Test', (100,220), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,255), 2) # and also draw the word Test

        cv2.imshow(windowName, smallFrame) # show the resized frame

        k = cv2.waitKey(1) 
        
        if k & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
