## OPM with Gunicorn and Nginx

### Tested Environment

**Linux**: vagrant box "bento/ubuntu-18.04"

**Python**: Python3.6.9

*According to* `flask --version`:

> Python 3.7.5
> Flask 1.1.1
> Werkzeug 0.16.0

**Nginx**: nginx/1.14.0 (Ubuntu)

**Gunicorn**: gunicorn (version 20.0.4)

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
  |--/etc/nginx/sites-available/opm # rm /etc/nginx/site-enabled/default
  |--/etc/nginx/sites-enabled/opm # floppy link to sites-available/opm
--/var/
  |--log/extraeyes/ # todo: change to opm
     |--app.log # create, ensure permission for www-data
     |--gunicorn.log # same as above
     |--nginx-error.log # floppy link to /var/log/nginx/error.log
```

### Gunicorn

#### /home/$user/opm/wsgi.py

```python
from app import app

if __name__ == "__main__":
    app.run()
```

### /etc/systemd/system/opm.service

```bash
# Flask, OPM, Gunicorn Service
# extraeyes is the name of the prototype. If that name is no longer referencenced in log or other directives, set to opm folder instead

[Unit]
Description=Gunicorn instance to serve Open Prose Metrics via Gunicorn and Flask
After=network.target

[Service]
User=vagrant
Group=www-data
WorkingDirectory=/home/vagrant/opm
ExecStart=/usr/local/bin/gunicorn --access-logfile /var/log/extraeyes/gunicorn.log --workers 3 --bind unix:/tmp/gunicorn.sock -m 007 wsgi:app


[Install]
WantedBy=multi-user.target
```

#### /etc/nginx/sites-available/opm

```nginx
server {
    listen 80;
    server_name openprosemetrics www.openprosemetrics;

    location / {
        include proxy_params;
        proxy_pass http://unix:/tmp/gunicorn.sock;
    }
}
```

### Deployment

#### Simple Vagrantfile

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-18.04"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  # config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.provision "file", source: "opm", destination: "~/opm"
  #config.vm.provision "file", source: "flask-nginx-gunicorn/gunicorn/systemd/gunicorn.service", destination: "/etc/systemd/system/gunicorn.service"
  #config.vm.provision "file", source: "flask-nginx-gunicorn/nginx/opm", destination: "/etc/nginx/sites-available/opm"
  config.vm.provision "shell", path: "deploy-opm.sh"
end
```

#### Initialization

*Script or sequence for getting prereqs. Aiming for provision script for vagrant*

*This is a prototype for a basic vagrant box for this application.*

Replace opt with vagrant or other user home.

```bash
#!/bin/sh
apt-get update
apt upgrade -y
apt-get install -y python3 python3-dev python3-pip ipython3 python3-pycurl libenchant-dev unzip openjdk-8-jre-headless git unzip libenchant-dev libpoppler-dev 
update-alternatives --install /usr/bin/python python /usr/bin/python3 10
update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10
wget https://nlp.stanford.edu/software/stanford-ner-4.0.0.zip
unzip stanford-ner-4.0.0.zip
mv stanford-ner-4.0.0 /usr/share/stanford-ner
pip install gunicorn
mkdir /var/log/extraeyes &&  sudo chmod 777 /var/log/extraeyes
mv opm/ /opt/opm
chmod -R 777 /opt/opm
cd /opt/opm/
pip install -r requirements.txt
python -m nltk.downloader -d /usr/share/nltk_data stopwords words punkt brown vader_lexicon averaged_perceptron_tagger maxent_ne_chunker
echo "t = create_tagger()" >> postagger.py
echo "save_tagger(t)" >> postagger.py
python postagger.py
#python seed_database.py
mv /opt/opm/opm.service /etc/systemd/system/opm.service
systemctl enable opm.service
systemctl start opm.service
rm /home/vagrant/stanford-ner-4.0.0.zip
apt-get clean
```

### Remaining Questions

* **gunicorn v uwsgi**? uwsgi has not been successfully implemented with nginx for this

* python 3.7 for ubuntu 20.04

* what about python3.8? Not supported by uwsgi. what about gunicorn

### ToDo

* change log directory to opm instead of extraeyes

* find way to get app.log from flask logged activity for running with gunicorn
