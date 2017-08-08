Installation
==================

## Requirements

1. Python 2.7x
2. MongoDB

## Configuring dev environment
### For Linux, PIP an Virtual Environment Setup

    sudo apt-get install python-pip python-dev build-essential
    sudo pip install --upgrade pip
    sudo pip install virtualenvwrapper

### For MacOSX, PIP and Virtual Environment Setup

For MacOSX users, `Homrbrew` and `XCode command line tools` are needed.

HomeBrew setup:

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

XCode command line tools setup:

    xcode-select --install

And Then:

    sudo easy_install pip
    sudo apt-get install python-pip
    sudo pip install --upgrade pip
    sudo pip install virtualenvwrapper
  
## Create Virtual Environment

[virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/index.html) is a set of extensions to Ian Bicking’s virtualenv tool. The extensions include wrappers for creating and deleting virtual environments and otherwise managing your development workflow, making it easier to work on more than one project at a time without introducing conflicts in their dependencies.

To create virtual environment run 

```
mkvirtualenv argumanorg
```

To enable virtual environment in a new console run 
```
workon argumanorg
```

## Clone and configure project

You need to clone project and install requirements

    git clone git@github.com:arguman/arguman.org.git
    cd arguman.org
    pip install -r requirements.txt

Then you need to configure it. Copy and fill in the provided settings template:

    cp web/main/settings_local.py.ex web/main/settings_local.py

## MongoDB database

[Install MongoDB](http://docs.mongodb.org/manual/installation/).
    
## Configure Postgres database

If the default configuration of using main `postgres` user and db won't work because of the access rights 
or if you prefer to have a separate database for arguman then you have to create it and configure it in `settings_local.py`.
 
    sudo -u postgres psql -c "CREATE USER arguman WITH PASSWORD 'arguman';"
    sudo -u postgres createdb -O arguman arguman -E utf-8

## Setup redis [optional]

Redis can be used for caching data in the web application. 

For MacOSX, setup Redis

    brew install redis-server

For Linux setup Redis (For latest version of Redis https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis)

    sudo apt-get install redis-server

Start Redis:

    redis-server
    
For the app to use redis as a cache you have to define `CACHES` settings in your `settings_local.py` file. 

## Create an admin user and run the website!

    cd web
    python manage.py migrate
    python manage.py createsuperuser
    python manage.pr runserver

## The End
:tada: