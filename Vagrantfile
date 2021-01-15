# -*- mode: ruby -*-
# vi: set ft=ruby :
$ram = 8096
$cpus = 4
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-18.04"
  config.vm.network "forwarded_port", guest: 80, host: 8081
  config.vm.network "forwarded_port", guest: 5000, host: 5001
  config.vm.provision "shell", path: "deploy.sh"
  config.vm.provision "shell", path: "wsgi-install.sh"
  config.vm.provider :virtualbox do |vb|
  #   # Don't boot with headless mode
  #   vb.gui = true
  #
  #   # Use VBoxManage to customize the VM. For example to change memory:

    vb.customize ["modifyvm", :id, "--memory", $ram, "--cpus", $cpus]
  end
end
