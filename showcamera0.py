# showcamera0.py

# This is perhaps the simplest possible program to display the video from an rtsp IP camera

import cv2
import config # config.py contains the rtsp url for the camera

rtsp = config.geturl() # get the configured url for the camera

# Open the video window and place it somewhere convenient
windowName = "Video Window" # the name of the window identifies it for later
cv2.namedWindow(windowName)
cv2.moveWindow(windowName, 800, 100) # this is to put the window in a desired position (it is a bit wacky)
cv2.setWindowProperty(windowName, cv2.WND_PROP_TOPMOST, 1) # optionally put the window on top

def main():

    cap = cv2.VideoCapture(rtsp) # Open the video stream from the camera
    
    while cap.isOpened():
        ret, frame = cap.read() # read the frame from the camera (waits until it is read)

        if not ret:
                break # exit if the camera stops sending
        
        cv2.imshow(windowName, frame) # show the video frame in the window

        k = cv2.waitKey(1) # see if any keypress (this is also necessary to display the video)
        
        if k & 0xFF == ord('q'): # quit the program if the key q is pressed
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
