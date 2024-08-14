# Signal Processing for Condition Monitoring
This repository contains the signalprocessing.py file, which is a Python library for signal processing in condition monitoring.

This module is focused on the signal processing methods which are commonly used in vibration based condition monitorig. For example the processing methods used in MEV781 - Vibration Based Condition Montioring.

Last Update 14 August 2024.

# Installation
To use this library, clone the repository and import the signalprocessing.py file in your Python script.

# Errors:
Please feel free to contact me, Justin Smith, through 66smithjustin@gmail.com if you notice any issues.

# About the Author:
I am currently a mechanical engineering Masters candidate at the University of Pretoria performing research in the Center for Asset Integrity Management. I am focusing on vibration based condition monitoring systems for axial fans. Linkedin: https://www.linkedin.com/in/justin-s-507338116/

# To Do's
Add references for all the functions and ask Dr Diamond if i can publish the get_rpm BGC code
Add useful code from BTT test notebooks (such as the get_threshold function, get_dataframe function and so on)
Update the get_displacement_signal function to handle a MPR signal and not just an OPR signal
Update filter funtion to use filtfilt as its a function of past and future so the filter wont lag the input (https://stackoverflow.com/questions/13740348/how-to-apply-a-filter-to-a-signal-in-python/13740532#13740532)
might be a good idea to have more filtering options