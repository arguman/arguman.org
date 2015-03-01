Proje Kurulumu
==================

Gereksinimler

1. Python 2.7x
2. MongoDB

## Linux icin PIP ve Virtual Environment kurulumu

    sudo apt-get install python-pip python-dev build-essential
    sudo apt-get install python-pip
    sudo pip install --upgrade pip
    sudo pip install --upgrade virtualenv

## MacOSX icin PIP ve Virtual Environment kurulumu

MacOSX icin Homebrew ve XCode command line tools un kurulu olmasi gerekiyor.

HomeBrew kurulu degil ise su sekilde kurabilirsiniz.

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

XCode command line tools kurulu degil ise su sekilde kurabilirsiniz.

    xcode-select --install
    
Kurulumun geri kalani icin

    sudo easy_install pip
    sudo apt-get install python-pip
    sudo pip install --upgrade pip
    sudo pip install --upgrade virtualenv

Virtual Environment Olusturmak

    virtualenv argumanorg
    source argumanorg/bin/active

Projeyi klonlamak ve gereksinimlerini kurmak

    git clone git@github.com:arguman/arguman.org.git
    pip install -r arguman/requirements.pip

MongoDB yi calistirmak (http://docs.mongodb.org/manual/installation/)
    
    mongod

Projeyi Calistirmak
    
    python manage.py migrate
    python manage.pr runserver

