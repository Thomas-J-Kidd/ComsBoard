# This LoRa Branch has all the code for the Raspberry Pi 3b+ that runs on most operating systems. 

## Structure
There are two folders in this directory
- docs
- RpiTesting

### docs
docs hosts a series of files for documenting your python. within docs you will see two different folders:
- build
- source

#### Overview
The build folder has an html folder inside it that has in index.html file. By double clicking on this file you will pull up the docummentation of the code. 

The source folder houses the configuration file that dictates how the documentation is generated. It should be configured, but if you need please reach out to thomas.kidd@okstate.edu

#### How to update documentation

This documentation tool is using Sphynx and two plugins called: 
- myst_parser
- autapi

In every function you can start a docstring ```""" write your documentation here """```
For more syntax look up sphynx python syntax as well as myst_parsers

TO update the html page make sure you are in the docs directory, then type:
- linux: ```make html```
- windows: ```make.bat```

This will update the html file

### RpiTesting
This folder hosts the different modules and their respective master and slave devices. Each master and slave folder will have a src folder where the python code is housed. Please look at the html file for the more specific documentation on the code. 
