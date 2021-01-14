# Open Prose Metrics

Feed this web application a file, url, or paste with prose in English and it will provide data from which an assessment can be made, for the purposes of:

* planning substantive revision

* setting writing goals or objectives, as case managers might do

* track a your progress toward a writing objective or accomplishing a challenge

* or, track the progress of a student toward written langauge goals, or written expression or mechanics objects.

* Generate speech from text for proofing or an accessibility toool (downloadable as mp3)

Python3, Flask, Apache2, mod_wsgi, stanford_ner, and NLTK are involved. The repo includes a Vagrantfile (contents at the end of this document). 

However, the other tools can be used to install on Ubuntu 18.04, or adapted for other releases and distros.

<img src="/home/rik/test-opm-vagrant/open-prose-metrics/img/index.png">

<img src="/home/rik/test-opm-vagrant/open-prose-metrics/img/concision-precision.png">

### Tested Environment

**Linux**: vagrant box "bento/ubuntu-18.04"

**Python**: Python3.7.5

*According to* `flask --version`:

> Python 3.7.5
> Flask 1.1.1
> Werkzeug 0.16.0

**Apache2**

**mod_wsgi** 7.7.1

## Try It

File structure, rough deployment script, building mod_wsgi from source, and a sample apache2 virtual server conf for the application are provided below.

demo server at <https://extraeyes.gonzotraining.com>. *interface is a bit different than what's provided here.*

Install for your school or test env or home with this repo.

The deployment script assumes /vagrant exists and the user is vagrant.

However, there are vars at the top of the script. Replace `/vagrant` with `$installer_dir` and set the var to the path to your target directory without a trailing slash (such as `/var/www/html/open-prose-metrics`). A simple change is necessary for the alias definition in the virtual host config (below) as well.



### File Structure

```
/
--/home/$USER/opm/ # app home. No ___init__.py present.
  |--wsgi.py # gunicorn wsgi file
  |--input/read_document # from opm/app/input/ directory, not opm/opm/input/
--/tmp/
  |--gunicorn.sock # created dynamically as needed. Will have permissions from service definition(?)
--/usr/share/
  |--stanfor-ner/ # create using sudo as $USER (owner of app); 
  |--nltk-data/ # create directory, then python -m nltk.downloader -d /usr/share/nltk_data stopwords words punkt brown vader_lexicon averaged_perceptron_tagger maxent_ne_chunker
--/etc/
  |--systemd/system/gunicorn.service # specifically for opm
  |--/etc/apache2/sites-available/opm.conf # 
--/var/
  |--log/opm/ # todo: change to opm
     |--error.log # for the apache vhost
  |--log/extraeyes/
     |--app.log # flask output to stdout and stderror when running with flask app in venv
```

### Draft Deployment: Flask, Apache2 w mod_wsgi (ubuntu-18.04)

application user: vagrant

```bash
#!/bin/bash -ex


INSTALLER_DIR="/vagrant"
TARGET_DIR="/var/www/html/open-prose-metrics"
APP_OWNER="vagrant"
APP_GROUP="www-data"
LOG_DIR="/var/log/opm"
VENV="/var/www/html/open-prose-metrics/virtualenv"
NER_DIR="/usr/share"
NLTK_DATA_DIR="/usr/share/nltk_data"

# dpkg-reconfigure tzdata (automation?)
ln -fs /usr/share/zoneinfo/US/Eastern /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# Repository - General
echo "Install from Ubuntu Package Manager"
apt update && apt upgrade -y
apt install -y linux-headers-$(uname -r)
apt install -y apache2 python3 python3-dev python3-pip
apt install -y python3.7 python3.7-dev
apt install -y libenchant-dev unzip openjdk-8-jre-headless
# Repository - depends for pycurl
apt install -y libcurl4-openssl-dev libssl-dev
# Repository - for scipy and numpy
apt install -y libatlas-base-dev
# Repository - possibly required by numpy and scipy
apt install -y libpython3.7 libpython3.7-dev gcc gfortran python-dev libopenblas-dev liblapack-dev cython
# Repository - compiling mod-wsgi for python: dependencies
apt install -y apache2-dev

# Stanford NER (Required by nltk for opm NER)
wget https://nlp.stanford.edu/software/stanford-ner-4.0.0.zip
unzip stanford-ner-4.0.0.zip -d $NER_DIR
chown -R $APP_OWNER:$APP_GROUP $NER_DIR
mv $NER_DIR/stanford-ner-4.0.0 $NER_DIR/stanford-ner


# depends for pycurl
apt install -y libcurl4-openssl-dev libssl-dev
# Pip: system-wide dependencies
echo "Get Pip for Python3.7"
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.7 get-pip.py
pip3.7 install wheel virtualenv ipython
echo "Create VENV"
virtualenv -p python3.7 $VENV
source $VENV/bin/activate
echo "Install from venv pip"
pip install -r /vagrant/opm/requirements.txt
# opm
echo "Copy App Folder"
cp -r /vagrant/opm $TARGET_DIR/opm # move app folder
#Create and set permissions
echo "Create Files and Directories and Set Permissions"
mkdir /var/log/extraeyes /var/log/opm /home/$APP_OWNER/.plotly
touch /var/log/extraeyes/app.log
chown -R $APP_OWNER:$APP_GROUP /var/log/extraeyes
chown -R $APP_OWNER:$APP_GROUP /var/log/opm
chown -R $APP_OWNER:$APP_GROUP /home/$APP_OWNER/.plotly
chmod 775 /home/$APP_OWNER/.plotly
chown -R $APP_OWNER:$APP_GROUP $TARGET_DIR
#nltk_data
echo "Fetching NLTK data"
python -m nltk.downloader -d /usr/share/nltk_data stopwords words punkt brown vader_lexicon averaged_perceptron_tagger maxent_ne_chunker #for ner
echo "Pre-create Postagger (depends on stanford NER)"
chown -R $APP_OWNER:$APP_GROUP $NER_DIR/stanford-ner
cd $TARGET_DIR/opm && python postagger.py
echo "Seeding Database and Testing Backend"
cd $TARGET_DIR/opm && python seed_database.py
echo "Configuring Apache2"
cp $INSTALLER_DIR/opm-configs/etc/apache2/sites-available/*.conf /etc/apache2/sites-available/
sed -i "s|{{ owner }}|$APP_OWNER|" /etc/apache2/sites-available/opm.conf
sed -i "s|{{ group }}|$APP_GROUP|" /etc/apache2/sites-available/opm.conf
a2dissite 000-default
a2ensite opm.conf
apt clean
#systemctl reload apache2
# END - mod_wsgi will be called
echo "Finished. Next, wsgi-install will be called to compile, install mod_wsgi and reload apache2"
```

## Configure, Make, Install mod_wsgi

```bash
cd /vagrant/
unzip /vagrant/4.7.1.zip
cd mod_wsgi-4.7.1/
./configure --with-python=/usr/bin/python3.7
make
make install

#cp /usr/lib/apache2/modules/mod_wsgi.so /etc/apache2/modules/
chmod 644 /usr/lib/apache2/modules/mod_wsgi.so
systemctl reload apache2
```

## http server conf apache2

```apacheconf
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so

<VirtualHost *>
        ServerName blah.com
        ServerAlias opm.blah.com
        ServerAlias essayeyes.com
        #WSGIDaemonProcess opm user={{ owner }} group={{ group }} threads=5
        WSGIDaemonProcess opm user=vagrant group=www-data threads=5 python-path=/var/www/html/open-prose-metrics/opm:/var/www/html/open-prose-metrics/virtualenv/lib/python3.7/site-packages
        WSGIScriptAlias / /var/www/html/open-prose-metrics/opm/opm.wsgi
        <Directory /var/www/html/open-prose-metrics>
                WSGIProcessGroup opm
                WSGIApplicationGroup %{GLOBAL}
                #Order deny,allow
                Allow from all
        </Directory>
        ErrorLog /var/log/opm/error.log
</VirtualHost>
```

### Sample Vagrant File

```ruby
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

    vb.customize ["modifyvm", :id, "--memory", "1024", "--cpus", "2"] # once installed, 2048 is ok. One vcpu is file
  end
end

```

&copy; rik goldman, MIT LICENSE

High-school students at Chelsea School in Hyattsville, MD, gave encouragement and supported initial explorations into just how viable this project would be.
