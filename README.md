![Photo](projectphoto.jpg)


# SmartSecurityCamera
This is the reference material for the SmartSecurityCamera project and the presentation about it at MakerFaireRome's Maker Learn Session on November 11, 2021.

https://makerfairerome.eu/en/maker-learn-festival-en/?edition=2021&event_id=200063

The project is described on my website here:

https://rocketmanrc.com/smartsecuritycamerasystem.html

# Background
The way our house is situated it is not convenient to look out the front over the driveway unless you sit on a chair near a window. This is frustrating and inconvenient for a number of reasons as you can imagine and not something that a Maker and electronics enthusiast should put up with!

My original solution a number of years ago was to install a weatherproof IP security camera looking out over the driveway allowing me to watch the video on my smart phone. This meant that I didn't have to sit in the living room waiting for a taxi or perhaps a package delivery. That was better than nothing however it was far less than I was hoping for.

The camera itself has the ability to detect motion and then send still images via FTP to a server as well as an email notification to an email address. The email notification is not very useful however because of the long and inconsistent delay and the fact that the image isn't included. 

The camera manufacturer provided a streaming service with "AI" for object detection however this required full time streaming to the cloud and a monthly charge that is small but not insignificant ($10 per month). This didn't appeal to me at all so I never bothered to try it. A fun fact is that the manufacturer no long mentions "AI" and only saves video clips initiated by the camera!

My original solution to all this then was to setup an FTP server and write some simple software implemented with Node-RED to check for the arrival of the still images and then use the Pushover notification service to send a notification with image to my phone. Then I could look at the real-time video on my phone if I wanted to.

This actually worked pretty well except for a couple of problems. The first is motion detection in the camera. If it is set sensitive enough to be useful then there are lots of false positives and during bad weather the notifications are constant resulting in having to disable them. Another problem  is the time delay between the camera detecting something and receiving the still image on your phone. This can be more than a minute meaning that by the time you start looking at the real-time video on your phone the subject of the notification is most likely long gone.

In early 2020 I discovered a node for Node-RED that can do Object Detection using TensorFlowJS CoCo SSD:

https://flows.nodered.org/node/node-red-contrib-tfjs-coco-ssd

This was a fantastic solution to the false notification problem. Just pass the still images as they appear on the server to the detector and only send notifications if there are objects detected!

This is what got me interested in machine learning for object detection and a desire to use it on the real-time video.

In October of last year (2020) I discovered the Google Coral TPU (Tensorflow Processing Unit) which held the promise real-time object detection on the video stream from the camera. On November 11, 2020 I had this working on an old Dell Server running Debian 10 Linux and the performance is amazing.

Alas the Coral TPU modules of all types are in very short supply and have been for quite a while. I have been told however by Seeed Studio the manufacturer of the modules that this is due to the demand for all machine learning related hardware so there is hope that this supply situation will be resolved sometime soon.

In the meantime I have spent a lot of effort to implement a version of my final solution that doesn't require the Coral TPU accelerator and uses uses Tensorflowlite on the CPU only. The downside that is that it can't handle more that about 5 video frames per second but that is still usable. When the Coral TPUs become available it is easy to upgrade and get object detection on every video frame (at least up to 15 frames per second which is typical from an IP camera).

My final note is that my preferred computing platform for this system right now is the Seeed Studio Odyssey X86 with the Coral Mini PCIe TPU. Here is a reference to this setup on their Wiki:

https://wiki.seeedstudio.com/Coral-Mini-PCIe-Accelerator-on-ODYSSEY-X86J4105/

![Photo](https://github.com/RocketManRC/SmartSecurityCamera/blob/master/odyssey2.jpeg)

# The Project
I am using MacOS Catalina for development and also for the livestream presentation but the servers I will be talking about run Debian 10 linux (including PiOS) and the notes for installing and running the sofware are for those systems.

This project uses Tensorflow Lite which is evolving constantly and makes projects obsolete quickly and also means that it is difficult to determine if the information that you find on the Internet is current or not.

What I have attempted to do here is to make example code that is simple and easy to understand and therefore easier to modify and to use in your own projects. 

The goal is to use machine learning to make a SmartSecurityCamera and not to become an data scientist!

I will be updating this respository frequently up until the day of my presentation and I'm sure afterwards as well as long as there is interest.

# Prerequisites for Debian 10 Linux (not needed for PiOS)
This section will save some head scratching if you are new to Debian 10 Linux. 

Debian 10 doesn't come with the command sudo which is kind of mind boggling to me however here is a good reference on how to install it:

https://www.linuxuprising.com/2019/09/fix-username-is-not-in-sudoers-file.html

Here is a summary:

$ su - (changes to root user and command prompt changes to #)<br>
\# apt install sudo<br>
\# usermod -aG sudo yourusername<br>
\# reboot

Git needs to be installed.

$ sudo apt update<br>
$ sudo apt upgrade<br>
$ sudo apt install git<br>

# Installing the Code
Either download the zip file or install using Git (preferred as there will likely be lots of changes):

git clone https://github.com/RocketManRC/SmartSecurityCamera.git

Most of the code is written in Python3 however in the directory ONVIF is a node.js script to search for cameras on your network. I spent a lot of time trying to figure out how to do this in Python however I couldn't come up with a good solution.

# ONVIF
ONVIF is the Open Network Video Interface Forum and a standard for accessing IP security cameras. In the directory ONVIF is a utility to search for cameras on your network and show the URLs that can be used to access the cameras.

The script is findurls.js and requires node.js to run it. This isn't installed with Debian linux by default and I install it by installing Node-RED which I use for many other purposes. The installation procedure for Node-RED is here:

https://nodered.org/docs/getting-started/raspberrypi

This is for the Raspberry Pi but it works fine on Debian 10, just say no to installing the Pi extensions.

To install the script, copy and paste the following lines in the terminal:

$ cd SmartSecurityCamera<br>
$ npm install

Then to run it:

$ npm start

This should find all the cameras on your network that support ONVIF and give the URLs for accessing them. If your cameras are password protected then edit the file config.js and insert your user and password information.

A note about using camera URLs:

If a camera is password protected then it will need the user name and password to be added to the URL. Here is a typical RTSP URL:

rtsp://192.168.7.94:8554/profile0

And here it is with the credentials added:

rtsp://user:password@192.168.7.94:8554/profile0

# Python
For the purpose of my presentation I have written several Python example programs that will be explained below.

Debian 10 Linux comes with two versions of Python installed, 2.7.16 and 3.7.3. Python3 is required for everything in this project and Pip3 is the package manager required. Here is the way to get everything setup properly:

$ sudo apt install python3-pip<br>
$ sudo apt install build-essential libssl-dev libffi-dev python3-dev

I usually use python3 virtual environments for development but on my servers I don't. The instructions for using virtual environments are here (as well as an explanation for the installation steps above):

https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-debian-10

For the rest of these project notes I am assuming that we are NOT using a virtual environment.

We need to install opencv-python and I have found that is best to use slightly older versions. By experiment I have settled on these:

Debian 10:<br>
$ pip3 install opencv-python==4.2.0.34

PiOS:<br>
$ pip3 install opencv-python==4.3.0.38<br>
May also need these:<br>
$ sudo apt-get install libatlas-base-dev<br>
$ pip3 install numpy --upgrade

We also need imutils (both Debian 10 and PiOS):

$ pip3 install imutils

Install the Tensorflow Lite Runtime with support for the Coral TPU even if you don't have one (both Debian 10 and PiOS)

$ echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list<br>
$ curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -<br>
$ sudo apt update<br>
$ sudo apt install python3-tflite-runtime

# The Python Example Code
NOTE: the tflite examples also have a version that has "coral" in the filename and they use the Coral TPU to show the performance difference when using the TPU.

For most of these examples and the final application there must be **two folders named 'record' and 'validated'** created in the application folder.

showcamera0.py - this is perhaps the simplest possible program to display the video from an rtsp IP camera!

showcamera1.py - this adds some basic functions to work with the video (resize and annotate) and also measure the frame rate from the camera which is necessary later for saving the video in files. It also resizes the video to reduce CPU usage as displaying the video is only really for debugging in this application.

showcamera2.py - this shows how to save the full size unannotated video in 5 minute segments

tflite0.py - this runs a tensorflowlite object detector on the camera image frames, shows the detection time and prints info about any objects detected. 

tflite1.py - here we switch to using a captured video file instead of the camera (which we will use from now on)

tflite2.py - now we annotate the found objects with bounding boxes and labels

tflite3.py - change to processing every third video frame to accomodate the Raspberry Pi 4

tflite4.py - same as tflite3.py except with the camera to check on the Pi4

# The Final Application
The final application runs very well on the Odyssey with the Coral Mini PCIe TPU. I haven't made any effort to test this without the TPU due to lack of time however I am pretty sure it can be made to run well enough on the Odyssey and the Raspberry Pi 4 by only processing every third frame as shown in the example tflite4.py.

Here are the features in this application:

- Full size video from the camera is saved in 5 minute segments in the 'record' folder. At the end of each segment if an valid object has been detected the file is renamed by appending a '-v' to the filename. If there is no valid object detection then the previous video file is deleted. The objective of this is to not save video if there is likely nothing of interest in it.
- For every video frame with a validated object detected in it, an image file (jpg) is saved in the 'validated' folder. This is done at most once a second. There is also a metadata file saved in json format that can be useful in downstream processing.
- There are some heruistics for determining what a valid object is. These are as follows:
  - There is a very crude check to exclude objects outside a boundary. In my case I am excluding part of the left side of the image and part of the top. This can be replaced with your own logic to satisfy your requirements.
  - A list of detected objects is kept and new objects are tested to see if they are the same and ignored if so. Being "the same" means that the two object's center location in the video frame and their size are the within 10% each other. This has worked well to deal with things like vehicles parked in the driveway which would otherwise cause constant detections.
  - If object is detected that is determined to be the same as one in the list then the timestamp of the one in the list is updated.
  - Objects that are stale meaning their timestamp hasn't been updated for over 10 minutes are deleted from the list.
  - No more than 5 person detections are considered valid per 5 minute video frame. This just reduces the number of repetitive detections and is dependent on the environment that the camera will be used in.

# IoT Integration
The key to integration with other "downstream" applications including IoT and Home Automation is to monitor the 'validated' folder for new images and metadata files. At the present time I have a simple Node-RED flow that monitors this folder and sends a Telegram Messenger notification with image that can be received on any smart phone as well as on a desktop computer or even another application running on some other computer anywhere connected to the Internet. This requires an account on Telegram of course (free) and the creation of a Telegram Bot. There is lots of information out there on how to do this and it is beyond the scope of this project to explain it.

Here is what the Node-RED flow looks like:

![Photo](node-red-camera-alert.jpg)

The code for this is in the file node-red-camera-alert.txt and can be imported into Node-RED with the import function.

The following nodes are required to be installed using the palette manager:
- node-red-contrib-telegrambot
- node-red-contrib-time-range-switch
- node-red-contrib-watch-director

The telegrambot node needs to be configured with the bot token and the message id and the watch-directory node needs to have the full path of the 'validated' folder.

# References
I have based my example code on the object detection example for the Raspberry Pi in the tensorflow repository on Github here:

https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi

This is hot off the press at less than one month old at the time of this writing (November 9, 2021). I made a few changes to the support code to better suit my examples and I changed from the EfficientDet model which is very slow to SSD MobileNet V2 which is what I have been using for the past year.

The object detection models for both CPU and TPU come from here:

https://coral.ai/models/object-detection/

