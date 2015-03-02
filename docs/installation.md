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

MacOSX için `Homrbrew` ve `XCode command line tools` un kurulu olmasi gerekiyor.

HomeBrew kurulu değilse şu sekilde kurabilirsiniz.

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

XCode command line tools kurulu değilse şu şekilde kurabilirsiniz.

    xcode-select --install
    
Kurulumun geri kalanı için

    sudo easy_install pip
    sudo apt-get install python-pip
    sudo pip install --upgrade pip
    sudo pip install --upgrade virtualenv

Virtual Environment Oluşturmak

    virtualenv argumanorg
    source argumanorg/bin/active

Projeyi klonlamak ve gereksinimlerini kurmak

    git clone git@github.com:arguman/arguman.org.git
    pip install -r arguman/requirements.pip

MongoDB yi çalıştırmak (http://docs.mongodb.org/manual/installation/)
    
    mongod

Projeyi Çalıştırmak
    
    python manage.py migrate
    python manage.pr runserver

