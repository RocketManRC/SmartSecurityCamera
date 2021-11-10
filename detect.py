import collections
import cv2
import time
import math
#import numpy as np
import os
#import re
#import tflite_runtime.interpreter as tflite
import json
#import copy
from dataclasses import dataclass
#from typing import List
import platform
import imutils 
import config 
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils
import traceback

rtsp = config.geturl() 

model_path = 'ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite'

isMacOS = (platform.system() == 'Darwin') # to detect if we are on the development platform (in my case)

avipath = './record/' 
detpath = './validated/'

options = ObjectDetectorOptions(
    num_threads=2,
    score_threshold=0.7,
    max_results=3,
    enable_edgetpu=True)

detector = ObjectDetector(model_path=model_path, options=options)

Object = collections.namedtuple('Object', ['id', 'score', 'bbox'])

validNames = ("person", "car", "truck", "cat", "dog", "bicycle", "motorcycle", "bird")

@dataclass
class DetectedObj:
    id: int
    size: float
    xcenter: float
    ycenter: float
    timestamp: float

    def __eq__(self, other):
        """Overrides the default implementation"""
        # This checks if the ids are the same and the size and position are are within 10%
        # Doing an 'in' on a list of these will use this for comparison.
        result = (self.id == other.id) 
        result = result and (abs(self.size - other.size) < self.size * 0.1)
        result = result and (abs(self.xcenter - other.xcenter) < self.xcenter * 0.1) 
        result = result and (abs(self.ycenter - other.ycenter) < self.ycenter * 0.1)
        return result

objList = []

def main():
    cap = cv2.VideoCapture(rtsp)
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    avifn = avipath + time.strftime("rec-%Y%m%d-%H%M%S.avi")
    lastFileTime = time.time()
    print(avifn) 
    out = cv2.VideoWriter(avifn, fourcc, 15.0, (int(cap.get(3)), int(cap.get(4))))

    frameCount = 0
    frameTotalCount = 0
    startTime = time.time()
    lastFrameTime = startTime
    initTime = startTime
    lastObjTime = startTime
    imageCounter = 0
    showVideo = 1
    fps = 15.0
    isValidated = 0
    aviLastFn = ""
    personImageCount = 0

    while cap.isOpened():
        frameCount += 1
        frameTotalCount += 1
        currentTime = time.time()
        
        ret, frame = cap.read()
        
        if not ret:   # and exist the loop to end if no frame
            break        
           
        detections = detector.detect(frame)

        if isMacOS:
            scale_percent = 50 # percent of original size
        else:
            scale_percent = 25 # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)

        if detections:
            annotatedFrame = utils.visualize(frame, detections) # use the visualize utility to show the objects
            smallFrame = imutils.resize(annotatedFrame, width=width, height=height) 
        else:
            smallFrame = imutils.resize(frame, width=width, height=height)

        # We want to keep track of detected and validated objects here.
        # An object can be identified by its type (id), its size (within 10% ?) and its 
        # centre location (within 10% ?). It also needs a timestamp so it can be
        # detected as stale and deleted. Here is the algorithm:
        # When an object is detected check and see if it is in the list and if so
        # update its timestamp. If not add it to the list and set the isValidated flag.
        # For cleanup purposes every time a detected object is searched for remove
        # objects that are stale (say older than 10 minutes or so).
        # If the object is a person I only want to save one image every video segment
        # to avoid the problem with being flooded by messages when someone is standing
        # in the driveway. If it is something else like a car or truck that is stationary there won't be 
        # multiple messages anyway.
        
        currentTime = time.time()

        if detections and currentTime - lastObjTime > 1.0:
            inRange = 0
            for obj in detections:
                xsize = (obj.bounding_box.right - obj.bounding_box.left)
                xcentre = obj.bounding_box.left + xsize / 2
                ysize = (obj.bounding_box.bottom - obj.bounding_box.top)
                ycentre = obj.bounding_box.top + ysize / 2
                size = xsize * ysize

                label = obj[1][0][0]
                id = obj[1][0][2]

                invalidPerson = (label == 'person' and size < 0.01) # and invalid person if size is too small
                
                inBoundary = obj.bounding_box.bottom > 0.20 and obj.bounding_box.right > .32 # crude boundary limits for field of view

                if inBoundary and label in validNames and not invalidPerson: # filter out invalid objects
                    detectedobj = DetectedObj(id, size, xcentre, ycentre, time.time())

                    if detectedobj in objList:
                        # our detected object is in the object list so update its timestamp
                        try:     
                            for i in range(len(objList)):
                                if objList[i] == detectedobj:       
                                    objList[i].timestamp = time.time()
                                    print('Object timestamp updated')
                                    break;
                        except Exception:
                            traceback.print_exc()
                    else:
                        objList.append(detectedobj)
                        if id == 0 and personImageCount > 4: # save maximum of 5 images per video segment
                            print("Not saving image because more than 5 saved for this video segment...")
                        else:
                            if id == 0:
                                personImageCount = personImageCount + 1 # only 5 person images per video segment
                            detfn = detpath + time.strftime("det-%Y%m%d-%H%M%S.jpg")
                            print(detfn) 
                            cv2.imwrite(detfn, frame)
                            metafn = detfn.replace("jpg", "json") # create the metadata filename
                            jsonString = json.dumps(detectedobj, default = lambda x: x.__dict__)
                            text_file = open(metafn, "w")
                            text_file.write(jsonString)
                            text_file.close()
                            lastObjTime = currentTime
                            isValidated = 1 # set this so we can mark the current video as validated
        
        # Print out the frame count every 5 seconds
        frameTime = time.time()
        lastFrameTime = frameTime
        elapsedTime = frameTime - startTime
        if elapsedTime >= 5:
        	startTime = frameTime
        	fps = frameCount / elapsedTime
        	frameCount = 0;
        	print('fps: ', fps)
        
        # start a new output file every 5 minutes       
        if frameTime - lastFileTime > 5 and math.floor(frameTime - initTime) % 300 == 0:
            out.release() # close off the file
            if isValidated:
                print('Video has validated objects!')
                fn, ext = os.path.splitext(avifn)
                fn += '-v' # append '-v' to mark as validated
                avivfn = fn + ext
                os.rename(avifn, avivfn) # rename the file to show it has validated objects
                avifn = avivfn # we changed the name so we want to remember that later instead
                isValidated = 0                
            elif not '-v' in aviLastFn and os.path.exists(aviLastFn): # this was a file with no objects detected
                # delete the last file if it had no objects detected either
                os.remove(aviLastFn)
                #print('looking for mice, temporarily not removing files...')
                
            aviLastFn = avifn 
                    
                
            lastFileTime = time.time()
            avifn = avipath + time.strftime("rec-%Y%m%d-%H%M%S.avi")
            print(avifn) 
            personImageCount = 0 # reset flag to allow a person image for this video segment
            out = cv2.VideoWriter(avifn, fourcc, 15.0, (int(cap.get(3)), int(cap.get(4))))

            # delete object in list that are older than 10 minutes
            for o in objList:
                if time.time() - o.timestamp > 600: 
                    try:
                        idx = objList.index(o)
                        del objList[idx]
                        print("deleted object from list")
                        print(o)
                    except:
                        print("can't find or delete object from list")               
                        print(o)

        # I added this to resize the viewed image for display (make it bigger on the MacOS development system)
        if showVideo:
            cv2.imshow('frame', smallFrame)
 
        # save the recording    
        out.write(frame)
            
        k = cv2.waitKey(1) # from a camera process as fast as they get here
        
        if k & 0xFF == ord('q'):
            break
        if k & 0xFF == ord('0'):
            showVideo = 0
        if k & 0xFF == ord('1'):
            showVideo = 1
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(imageCounter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            imageCounter += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
