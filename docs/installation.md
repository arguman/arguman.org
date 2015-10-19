Project Setup
==================

Requirements

1. Python 2.7x
2. MongoDB
3. Redis

## Environment Setup for Linux

    sudo apt-get install python-pip python-dev build-essential
    sudo apt-get install python-pip
    sudo pip install --upgrade pip
    sudo pip install --upgrade virtualenv

Install Mongodb:
    sudo apt-get install mongodb

Install Redis:

    sudo apt-get install redis-server

Create a virtual environment

    virtualenv argumanorg
    source argumanorg/bin/active

Clone project and install requirements

    git clone git@github.com:arguman/arguman.org.git
    pip install -r arguman/requirements.pip


## Environment Setup for Mac OSX 

Note for El Capitan users: El Capitan introduces a new security feature called System Integrity Protection. You may need to disable this. See: https://github.com/Homebrew/homebrew/blob/master/share/doc/homebrew/El_Capitan_and_Homebrew.md 

You need `Homebrew` and `Xcode Command Line Tools`

Install homebrew:

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install Xcode Command Line Tools

    xcode-select --install

Install and start mongodb
    
    brew install mongodb 

Install Redis

    brew install redis-server

Install PIP and VirtualEnv

    sudo easy_install pip
    sudo pip install --upgrade pip
    sudo pip install --upgrade virtualenv

Create a virtual environment

    virtualenv argumanorg
    source argumanorg/bin/active

Clone project and install requirements

    git clone git@github.com:arguman/arguman.org.git
    pip install -r arguman/requirements.pip


## Run Project

    
    python manage.py migrate
    python manage.pr runserver

