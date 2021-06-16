# PostIt
## Small blog-platform 

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Small social media where you can create and post some notes with users and groups

## Features

- User`s creation
- Make a posts with the pictures inside
- Comment posts of another authors and follow them
- Checking and reading all posts of authors
- Posts editing and group creation

## Tech
- Phyton 3.7

## Installation

All important installations you can find in requirements.txt

Install the dependencies and start the server.

```sh
install requirements.txt
pip install -r requirements.txt
```

After installation of the dependences and initialization you have to make migrations (don`t forget to install environment)

```sh
python manage.py makemigrations
python manage.py migrate
```

Create an administrator to have an access for administration panel

```sh
python manage.py createsuperuser
```

Start the application

```sh
python manage.py runserver
```




