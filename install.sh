#!/usr/bin/env bash
set -e
sudo apt-get update
sudo apt-get install -y python python-pip python-dev build-essential mongodb redis-server
sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv
cd ~
virtualenv .virtualenv
. .virtualenv/bin/activate
cd /vagrant
pip install -r requirements.txt
echo ". ~/.virtualenv/bin/activate" >> ~/.profile
echo "cd /vagrant/web" >> ~/.profile
