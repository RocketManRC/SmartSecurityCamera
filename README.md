# SmartSecurityCamera
This is the code for the SmartSecurityCamera project and the presentation about it at MakerFaireRome's Maker Learn Session on November 11, 2021. I am using MacOS Catalina for development and also for the livestream presentation but the servers I will be talking about run Debian 10 linux (including PiOS) and the notes for installing and running the sofware are for those systems.

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
Either download the zip file or install using Git (preferred):

git clone https://github.com/RocketManRC/SmartSecurityCamera.git

Most of the code is written in Python3 however in the directory ONVIF is a node.js script to search for cameras on your network. I spent a lot of time trying to figure out how to do this in Python however I couldn't come up with a good solution.

# ONVIF
ONVIF is the Open Network Video Interface Forum and a standard for accessing IP security cameras. In the directory ONVIF is a utility to search for cameras on your network and show the URLs that can be used to access the cameras.

The script is findurls.js and requires node.js to run it. This isn't installed with Debian linux by default and I install it by installing Node-RED which I use for other purposes. The installation procedure for Node-RED is here:

https://nodered.org/docs/getting-started/raspberrypi

This is for the Raspberry Pi but it works fine on Debian 10, just say no to installing the Pi extensions.

To install the script copy and paste the following lines in the terminal:

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

# Python Code
For the purpose of my presentation I have written several Python programs that will be explained below.

Debian 10 Linux comes with two versions of Python installed, 2.7.16 and 3.7.3. Python3 is required for everything in this project and Pip3 is the package manager required. Here is the way to get everything setup properly:

$ sudo apt install python3-pip<br>
$ sudo apt install build-essential libssl-dev libffi-dev python3-dev

I usually use python3 virtual environments for development but on my servers I don't. The instructions for using virtual environments are here (as well as an explanation for the installation steps above):

https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-debian-10

For the rest of these project notes I am assuming that we are NOT using a virtual environment.

We need to install opencv-python and I have found that is best to use slightly older versions. By experiment I have settled on these:

Debian 10:
$ pip3 install opencv-python==4.2.0.34

PiOS:
$ pip3 install opencv-python==4.3.0.38

We also need imutils:

$ pip3 install imutils
