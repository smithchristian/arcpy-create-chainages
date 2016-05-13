# create-chainages

This project is designed to create chainages for projects utilising ArcGIS 10.x , Arcpy and Python. 

### Description of Project Contents

    create-chainage
    |   +-- create_chainages.tbx
    |   +-- .gitignore
    |   +-- __init__.py
    |   +-- LICENCE.TXT
    |   +-- main.py
    |   +-- README.MD
    |   +-- _modules
    |   |   +-- __init__.py
    |   |   +-- create_chainages.py
    |   +-- _test_data
    |   |   +-- testline.shp
 

**create_chainages.tbx:**

This ArcGIS toolbox acts as the interface for this project. In order to use this tool, you will need to have [ESRI's ArcGIS Desktop](http://www.esri.com/software/arcgis/arcgis-for-desktop) installed. For more information regarding the use of an ArcToolbox, please visit ["Using the ArcToolbox window"](http://resources.arcgis.com/EN/HELP/MAIN/10.2/index.html#//003q0000001m000000).

**main.py:**

This module is the main module for this project. This module pulls in the functions from create_chainages.py to help construct the chainages from a polyline.

**modules:**

This folder contains modules to assist in compiling chainages from polylines.

+ **create_chainages.py**

    This module contains the functions to compile the chainages from polylines.

**test_data:**

This directory contains all the data necessary to test the functionality of this project.

### Requirements

In order to run this project the following is required:

+ [ESRI's ArcGIS Desktop](http://www.esri.com/software/arcgis/arcgis-for-desktop), and
+ [Python 2.7x](https://www.python.org/download/releases/2.7/)


### Installation

1. Ensure that you have the required software prior to using this tool - see Requirements section.
2. Download and unzip or create a clone of this repository onto your system.
3. Open ArcGis Desktop 10.x session.
4. Once ArcGis Desktop is open, Open ArcToolbox.
5. Once the ArcToolbox window/tab has open, add the create_chainages.tbx from this project.
6. The toolboxes help documentation has been populated with information to assist in the tools useage.

### Usage
+ Currently this script is limited to ArcGIS for Desktop Advanced users only.
+ Polylines must be projected in to an appropriate coordinate reference system
+ Polylines must contain a text field called "Name". This field contains the name for each feature.
+ Currently this script will always start 0 chainage at the start of the line. It does not does not facilitate offsetting the start change value.
+ Testing has only been carried out on coordinate reference system in meters.
+ Testing of interval ranges has been conducted from 0.1m up to 20m.

### How to use the test data

1. Open ArcGIS Desktop 10.x.
2. Open ArcToolbox.
3. If the Create Chainage toolbox is not present, follow the installation steps, then open the Create Chainage tool.
4. When the Create Chainage window appears, populate the “Input Polyline Feature Class” field, with the shapefile located here: \create_chainages\test_data\testline.shp”.
5. In the “Output Location” field, you can either specify your own output folder or use this location “\create_chainages\test_data”.
6. In the “Distance (m) Between Points” field, enter an appropriate interval/distance between chainages.
7. Click “Ok”.
8. When the tool has finished processing, a new .gdb will be created in your specified output location containing the following outputs: original polyline(s), chainages and a copy of the original polyline(s) but as a measured route.
