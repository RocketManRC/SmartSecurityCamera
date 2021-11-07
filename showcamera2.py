# showcamera2.py

# Save the fullsize unannotated video to files in a local folder called record
# and start a new file every 5 minutes.

import cv2
import imutils 
import time 
import config 
import os # added to manage files
import math # for calculating when to start new files

fps = 15.0 # the desired frames per second for the output file (to match the camera rate)

rtsp = config.geturl() 

windowName = "Video Window Resized"
cv2.namedWindow(windowName)
cv2.moveWindow(windowName, 1600, 600)
cv2.setWindowProperty(windowName, cv2.WND_PROP_TOPMOST, 1)

def main():
    cap = cv2.VideoCapture(rtsp)

    # I have found that saving to AVI files gives the best overall performance in terms of
    # CPU usage and image quality as well as being supported cross platform with applications
    # like VLC.
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # Use the XVID codec to make an avi file
    fn = './record/' + time.strftime("rec-%Y%m%d-%H%M%S.avi") # make a timestamp to name the file
    lastFileTime = time.time()
    startTime = time.time()
    
    out = cv2.VideoWriter(fn, fourcc, fps, (int(cap.get(3)), int(cap.get(4)))) # save at fps frames per second
   
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
                break

        frameTime = time.time() # use this to calculate when to start a new file
        
        smallFrame = imutils.resize(frame, width=1000) 

        cv2.imshow('Video Window Resized', smallFrame) 

        # don't check time for 5 seconds (because time.time() returns seconds) then after 300 start a new file
        if frameTime - lastFileTime > 5 and math.floor(frameTime - startTime) % 300 == 0:
            out.release() # close off the current file
            avifn = './record/' + time.strftime("rec-%Y%m%d-%H%M%S.avi") # generate a new filename
            lastFileTime = time.time()            
            print(avifn) 
            out = cv2.VideoWriter(avifn, fourcc, fps, (int(cap.get(3)), int(cap.get(4)))) # open it

        out.write(frame) # save the video frame to the file

        k = cv2.waitKey(1) 
        
        if k & 0xFF == ord('q'):
            break

    cap.release()
    out.release() # close the video file
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
