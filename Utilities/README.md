# Web Interface for DoMo-Pred 

## About

This repository is used for my Google Summer of Code 2017 project that develop a web interface for DoMo-Pred.


* To change the result life (how long a result will be delete when its been generated), please modify the variable `VAR_RESULT_LIFE` in file `SessionManager.py`

##### This folder is used for store some help libaries. Pages descriptions are as below.

## Pages descriptions
- **SessionManager.py**:Module for management of  sessions of analyzing.
- **CallAnalyze.py**: Module which will help call functions in DoMo-Pred. THis module is the bridge between the web interface and the DoMo-Pred. 
- **CCleaner.py**: This is a job scheduler for cache clean up based on Advanced Python Scheduler.
- **ZipMaker.py**: Function in this module is used to make zip file from results.
- **globeVar.py**: Here stores some globe variables used to exchange data between modules.
- **message.py**: Stores tip/error message displayed to the user
- **graph.py**: functions used for generate network of an interaction.

## Realted Documents

None.
