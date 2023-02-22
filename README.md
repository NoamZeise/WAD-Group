# Setup (anaconda)

Run these commands to setup an anaconda virtual environment for the app.


We will use the latest python version.

`conda create -n froggr python=3.10`

Activate the virtual environment.

`conda active froggr`

Install Django package.  We will use the latest stable version.

`pip install django==4.1`

Install pillow (An imaging library).

`pip install pillow`

Now, if you navigate to the website folder, you should be able to run the server.

`python manage.py runserver`


# Project Layout

This is laid out very similarly to Rango. `froggr` is an app that 
is part of the `froggr_website` project. 
