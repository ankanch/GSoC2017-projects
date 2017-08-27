# Web Interface for DoMo-Pred 

## About

This repository is used for my Google Summer of Code 2017 project that develop a web interface for DoMo-Pred.

 For more information,please refer to the [Documents](#documents) section and the [External Link](#external-link) section.

You can find the live version here : [http://beta.baderlab.org](http://beta.baderlab.org) 

##### You can find more documents in related directories.

## Documents

* [Procedure of Web interface](https://docs.google.com/document/d/1Mxs1QFGY9P9gsiIp_eJzmWr3jVp3obnPCpP7bg-OfCs/edit?usp=sharing)

* [Web Interface Structure](https://docs.google.com/drawings/d/1qi1b4SFCYvlnH7GY6Xb6FxQY9YhwJtauFVaq_J4hUCE/edit?usp=sharing)

* [How to organize user upload files](https://docs.google.com/document/d/1APkUkN0uEzOe7zhLUL_Pja34OvYxDRr7CMukWNaqFUg/edit?usp=sharing)



## File and Folders

- **Cache**:Cache folder where to store user upload files and analyze result.
- **data**: Here is the folder to save built in data like PWMs and domain as well as network data.
- **DoMoPred**:The original DoMo-Pred source code and excuable files (Some changes made for web interface support).
- **static**:Flask default folder to store JavaScript and CSS.
- **templates**:Flask default folder to store HTML files.
- **Utilities**:Function which will help to manage session,call analyze functions and so on.
- **app.py**: This is the entry for the web interface, including start cache cleaner and loading balance.
- **index.py**:Flask view functions script where to perform rendering HTML file and process HTTP request.

## Making it runnable on the server

Before you start, you have to [download the database files from here](https://drive.google.com/drive/folders/0B1wYCRysoEhza1J0WmVHM3VNWmM?usp=sharing), due to the file size limits of Github repo.

It will be running on port 80, therefore, on the Ubuntu we have to stop Apache2 first by running command below in the terminal:

```shell
sudo systemctl stop apache2.service
```

then type and run command below:

```shell
sudo python app.py
```

The script will automatically dectect if it's on server or local machine. The web interface use gunicorn to balance the load.

##### In order to make it running in a productive envirement, you have to create a file named as `mode.server` in the root directory. We use this file to dectect if it's in debug mode or productive.

## Python Modules Needed

* networkx
* flask
* numpy
* scipy
* apscheduler
* gunicorn

## External Link

* [DoMo-Pred Website](http://www.baderlab.org/Software/DoMo-Pred)

* [Original Issue:Developing a web interface for DoMo-Pred, the protein interactions prediction tool](https://github.com/nrnb/GoogleSummerOfCode/issues/63)

* [Projects Link on GSoC 2017 Site](https://summerofcode.withgoogle.com/projects/#5045706436902912)

* [My Proposal:Developing a web interface for DoMo-Pred](https://storage.googleapis.com/summerofcode-prod.appspot.com/gsoc/core_project/doc/4956808348172288_1491032260_ProposalforDevelopingawebinterfaceforDoMo-Pred-NRNB-LongZhang_3.pdf?Expires=1495094303&GoogleAccessId=summerofcode-prod%40appspot.gserviceaccount.com&Signature=G7zxVNZpdiWA1tGfg%2FzYMQnWqKHZHsthUo0GUoY3uDWFrB4kW1LOvoHwhoEi7ntWMzi7DSAimiVsmC1jQLhMKN2Na8bTCKzFbCQXprxr6TOVHLWuWI2pWNZmOJm2C6mlLE3RpYIlhxwWaouE%2FJwvNd2k0DhqYVXWOsEWmXt%2B9HzB15Tx2BLa4wLeCrdWs9jouHoJx2uqHc8n1eJCgEbqbJ7WTJ%2B9r%2FmO1apJOuiM%2FPwZicilgaW4XJ5iWohXAgcce6gXUqFQt5yceYPcgU8Fvzt6nMNNkSxVk%2BM8ulFayMXRZP56OENtYBEJnuYUVbxXzQyd8UP%2FcXfOlgoGOSHSlw%3D%3D)
