# Froggr Django Webapp

A social media when people can post froggs(bloggs) that can be commented on and reacted to. 
People can maintain follow lists, search for froggs, and sort posts by various properties.


# Team Contributions

* Leon- the viewing of posts, followers and unfollowing users
* Sujay- nav bar, css styling
* Peter-sorting of posts, templates,css
* Tim-log in, sign up, being able to like posts, css style
* Noam- population script, models, ajax scrolling 


 
# Dependencies

* [jquery and ajax from google apis](https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js)
* [bootstrap](https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css)
* [fontawesome for icons](https://use.fontawesome.com/releases/v5.6.1/css/all.css)


# Project Layout

`froggr` is an app that is part of the `froggr_website` project.

* The `froggr/` folder holds the python files that are used by the froggr app
* The `static/` folder holds permanent files used by the website (images/css/js files)
* The `media/` folder holds transient files, like user submitted images.
* The `templates/` folder holds the html templates that are used by django to render pages.
* The `example-posts/` folder holds the text and images for the population script

# Using the population script

Make sure you are in froggr the virtulenv. If not, run `conda activate froggr`.

If you don't have a databsae yet run `python manage.py migrate`

Now you can run the population script from the root of the project using `python populate_froggr.py`.


If you want to clear the database run `python manage.py flush` and enter `yes` when prompted. 
Note that this will also delete any users you made to login with.


# Setup (anaconda)

Download this repository to your current directory

```
git clone https://github.com/NoamZeise/froggr_website.git
```

Run these commands to setup an anaconda virtual environment for the app.

We will use the latest python version.

```
conda create -n froggr python=3.10
```

Activate the virtual environment.

```
conda activate froggr
```

Install Django package.  We will use the latest stable version.

```
pip install django==4.1
```

Install pillow (An imaging library).

```
pip install pillow
```

Now, navigate to the website folder

```
cd froggr_website
```
Create the database
```
python manage.py migrate
```
populate the database
```
python populate_froggr.py
```
run the server

```
python manage.py runserver
```
Now the website should be accessible from localhost

# Making an admin account

Make sure you are in the froggr virtulenv. If not, run `conda activate froggr`.

Run 
```
python manage.py createsuperuser
```
Input a username, email and password when prompted.

Then start the server and use the login on the `/admin/` page.


# Running tests
Make sure you are in the froggr virtulenv, if not run `conda activate froggr`.


run the following to run all of froggr's tests
```
python manage.py test
```
