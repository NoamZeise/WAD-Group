# Setup (anaconda)

Download this repository to your current directory

`git clone https://github.com/NoamZeise/froggr_website.git`

Run these commands to setup an anaconda virtual environment for the app.

We will use the latest python version.

`conda create -n froggr python=3.10`

Activate the virtual environment.

`conda activate froggr`

Install Django package.  We will use the latest stable version.

`pip install django==4.1`

Install pillow (An imaging library).

`pip install pillow`

Now, if you navigate to the website folder, you should be able to run the server.

`cd froggr_website`

`python manage.py runserver`


# Project Layout

This is laid out very similarly to Rango. `froggr` is an app that 
is part of the `froggr_website` project. 


# admin details

* username: `admin`
* usermail: `admin@mail.com`
* password: `admin`
