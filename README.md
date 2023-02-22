# Setup (anaconda)

Run these commands to setup an anaconda virtual environment for the app.


We will use the latest python version.

`conda create -n froggr python=3.10`

Install Django package.  We will use the latest stable version.

`pip install django==4.1`

Install pillow (An imaging library)

`pip install pillow`


Now, if you navigate to the website folder, you should be able to run the server with 

`python manage.py runserver`
