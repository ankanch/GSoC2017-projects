# Web Interface for DoMo-Pred 

## About

This repository is used for my Google Summer of Code 2017 project that develop a web interface for DoMo-Pred.


* To change the result life (how long a result will be delete when its been generated), please modify the variable `VAR_RESULT_LIFE` in file `SessionManager.py`

##### This folder is used for store some help libaries. Pages descriptions are as below.

## Pages descriptions
- **_SessionManager.py_**:Module for management of  sessions of analyzing.
- **_CallAnalyze.py_**: Module which will help call functions in DoMo-Pred. THis module is the bridge between the web interface and the DoMo-Pred. 
- **_CCleaner.py_**: This is a job scheduler for cache clean up based on Advanced Python Scheduler.
- **_ZipMaker.py_**: Function in this module is used to make zip file from results.
- **_globeVar.py_**: Here stores some globe variables used to exchange data between modules.
- **_message.py_**: Stores tip/error message displayed to the user
- **_graph.py_**: functions used for generate network of an interaction.

## Realted Documents

None.
