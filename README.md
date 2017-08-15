# Web Interface for DoMo-Pred 

## About

This repository is used for my Google Summer of Code 2017 project that develop a web interface for DoMo-Pred.

 For more information,please refer to the [Documents](#documents) section and the [External Link](#external-link) section.

##### NOTE:this README is currently on building,things might change in the future.
##### You can find more documents in related directories.

## Documents

* [Web Interface Structure](https://docs.google.com/drawings/d/1qi1b4SFCYvlnH7GY6Xb6FxQY9YhwJtauFVaq_J4hUCE/edit?usp=sharing)
* [How to organize user upload files](https://docs.google.com/document/d/1APkUkN0uEzOe7zhLUL_Pja34OvYxDRr7CMukWNaqFUg/edit?usp=sharing)

## File and Folders

- **_Cache_**:Cache folder where to store user upload files.
- **_data_**: Here is the folder to save built in data.
- **_DoMoPred_**:DoMo-Pred source code and excuable files.
- **_static_**:Flask default folder to store JavaScript and CSS.
- **_templates_**:Flask default folder to store HTML files.
- **_Utilities_**:Function which will help to manage session,call analyze and so on
- **_index.py_**:Flask view functions script where to perform rendering HTML file and process HTTP request.

## Making it runnable on the server

It will be running on port 80, therefore, on the Ubuntu we have to stop Apache2 first by running command below in the terminal:

```shell
sudo systemctl stop apache2.service
```

then type and run command below:

```shell
sudo python index.py
```

##### Python Modules Needed

* networkx
* flask
* numpy
* scipy
* apscheduler
* gunicorn

##### In addition to make it running in a productive envirement, you have to create a file named as `mode.server` in the root directory. We use this file to dectect if it's in debug mode or productive.

## External Link

* [DoMo-Pred Website](http://www.baderlab.org/Software/DoMo-Pred)

* [Original Issue:Developing a web interface for DoMo-Pred, the protein interactions prediction tool](https://github.com/nrnb/GoogleSummerOfCode/issues/63)

* [Projects Link on GSoC 2017 Site](https://summerofcode.withgoogle.com/projects/#5045706436902912)

* [My Proposal:Developing a web interface for DoMo-Pred](https://storage.googleapis.com/summerofcode-prod.appspot.com/gsoc/core_project/doc/4956808348172288_1491032260_ProposalforDevelopingawebinterfaceforDoMo-Pred-NRNB-LongZhang_3.pdf?Expires=1495094303&GoogleAccessId=summerofcode-prod%40appspot.gserviceaccount.com&Signature=G7zxVNZpdiWA1tGfg%2FzYMQnWqKHZHsthUo0GUoY3uDWFrB4kW1LOvoHwhoEi7ntWMzi7DSAimiVsmC1jQLhMKN2Na8bTCKzFbCQXprxr6TOVHLWuWI2pWNZmOJm2C6mlLE3RpYIlhxwWaouE%2FJwvNd2k0DhqYVXWOsEWmXt%2B9HzB15Tx2BLa4wLeCrdWs9jouHoJx2uqHc8n1eJCgEbqbJ7WTJ%2B9r%2FmO1apJOuiM%2FPwZicilgaW4XJ5iWohXAgcce6gXUqFQt5yceYPcgU8Fvzt6nMNNkSxVk%2BM8ulFayMXRZP56OENtYBEJnuYUVbxXzQyd8UP%2FcXfOlgoGOSHSlw%3D%3D)


###### last modified: Aug 7 2017 CST