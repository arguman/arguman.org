Vagrant ile Projenin Kurulumu
==================

Eger daha önce eklenmediyse precise32 in eklenmesi gerekiyor.

    $ vagrant box add http://files.vagrantup.com/precise32.box --name precise32

VagrantFile in initialize edilmesi

    $ vagrant init precise32

Bu işlemden sonra proje klasörünüzde VagrantFile isminde bir dosya oluşmus olacak. Bu dosyayı açıp aşagıdaki şekilde comment li olan satırı,

    # config.vm.network "forwarded_port", guest: 80, host: 8080

aşağıdaki satırla değiştirmelisin.

    config.vm.network "forwarded_port", guest: 8000, host: 8000

Bu islemden sonra vagrant box imizi çalıştırabiliriz

    $ vagrant up


vagrant box imiza erişmek icin

    $ vagrant ssh

komutunu kullanabilirsiniz. Geri kalan kurulum işlemlerini [Proje Kurulum](installation.md) bölümündeki linux kurulumunu takip ederek tamamlayabilirsiniz.
