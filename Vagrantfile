# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-18.04"
  config.vm.network "forwarded_port", guest: 80, host: 8081
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  #config.vm.provision "file", source: "opm", destination: "~/opm"
  #config.vm.provision "file", source: "flask-nginx-gunicorn/gunicorn/systemd/gunicorn.service", destination: "/etc/systemd/system/gunicorn.service"
  #config.vm.provision "file", source: "flask-nginx-gunicorn/nginx/opm", destination: "/etc/nginx/sites-available/opm"
  config.vm.provision "shell", path: "deploy.sh"
  config.vm.provision "shell", path: "wsgi-install.sh"
  config.vm.provider :virtualbox do |vb|
  #   # Don't boot with headless mode
  #   vb.gui = true
  #
  #   # Use VBoxManage to customize the VM. For example to change memory:

    vb.customize ["modifyvm", :id, "--memory", "1024", "--cpus", "2"]
  end
end
