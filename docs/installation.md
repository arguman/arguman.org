Installation
==================

Requirements

1. Python 2.7x
2. MongoDB
3. Redis

## For Linux, PIP an Virtual Environment Setup

    sudo apt-get install python-pip python-dev build-essential
    sudo apt-get install python-pip
    sudo pip install --upgrade pip
    sudo pip install --upgrade virtualenv

## For MacOSX, PIP and Virtual Environment Setup

For MacOSX users, `Homrbrew` and `XCode command line tools` are needed.

HomeBrew setup:

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

XCode command line tools setup:

    xcode-select --install

And Then:

    sudo easy_install pip
    sudo apt-get install python-pip
    sudo pip install --upgrade pip
    sudo pip install --upgrade virtualenv

For Virtual Environment:

    virtualenv argumanorg
    source argumanorg/bin/active

And you need to clone project and install requirements

    git clone git@github.com:arguman/arguman.org.git
    cd arguman.org
    pip install -r requirements.txt

Start MongoDB (http://docs.mongodb.org/manual/installation/)

    mongod

For MacOSX, setup Redis

    brew install redis-server

For Linux setup Redis (For latest version of Redis https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis)

    sudo apt-get install redis-server

Start Redis:

    redis-server

Start the application of arguman:

    cd web
    python manage.py migrate
    python manage.pr runserver


The End
:tada: