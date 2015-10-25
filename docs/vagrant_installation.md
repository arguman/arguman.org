Vagrant Setup
=============

Download precise32 image and add it to your boxes.

    $ vagrant box add http://files.vagrantup.com/precise32.box --name precise32

Initialize a Vagrantfile

    $ vagrant init precise32

Change the following line on the Vagrantfile

	# config.vm.network "forwarded_port", guest: 80, host: 8080

to:

    config.vm.network "forwarded_port", guest: 8000, host: 8000

Start and login to the box:

    $ vagrant up
    $ vagrant ssh

Then follow the further instructions on [Project Setup](installation.md) page.