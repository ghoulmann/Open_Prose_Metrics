#!/bin/bash -ex

# dpkg-reconfigure tzdata (automation?)
ln -fs /usr/share/zoneinfo/US/Eastern /etc/localtime && dpkg-reconfigure -f noninteractive tzdata


#Ubuntu Packages


apt update && apt upgrade -y
apt install -y linux-headers-$(uname -r)
apt install -y apache2 libapache2-mod-wsgi python3 python3-dev python3-pip
apt install -y python3.7 python3.7-dev
apt install -y libenchant-dev unzip openjdk-8-jre-headless
# depends for pycurl
apt install -y libcurl4-openssl-dev libssl-dev
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.7 get-pip.py
# NER depends on NLTK having standford-ner
wget https://nlp.stanford.edu/software/stanford-ner-4.0.0.zip
#cp stanford-ner-4.0.0.zip /home/vagrant/
unzip stanford-ner-4.0.0.zip
mv stanford-ner-4.0.0/ /usr/share/stanford-ner
# python packages
## update-alternatives --install /usr/bin/python python /usr/bin/python3.7 10
## update-alternatives --install /usr/bin/pip pip /usr/bin/pip3.7 10
pip3.7 install wheel
mkdir -p /var/www/html/open-prose-metrics/opm
mkvirtualenv -p python3.7 /var/www/html/open-prose-metrics/virtualenv
source /var/www/html/open-prose-metrics/virtualenv/bin/activate
pip install -r opm/requirements.txt
mkdir /var/log/extraeyes/
mkdir /var/log/opm
touch /var/log/extraeyes/app.log
#touch /var/log/extraeyes/gunicorn.log
mkdir /home/vagrant/.plotly
chown -R vagrant:www-data /home/vagrant/.plotly
chmod 775 /home/vagrant/.plotly
chown -R vagrant:www-data /var/log/extraeyes
chown -R vagrant:www-data /var/log/opm
chown -R vagrant:www-data /var/www/html/open-prose-metrics

# nltk modules
python -m nltk.downloader -d /usr/share/nltk_data stopwords words punkt brown vader_lexicon averaged_perceptron_tagger maxent_ne_chunker
# parts of speech tagger
cd /var/www/html/open-prose-metrics/opm && python postagger.py && chown vagrant:www-data postagger.py
cd /var/www/html/open-prose-metrics/opm && python3.7 seed_database.py && chown vagrant:www-data shelve.db
# services


#cp /vagrant/flask-nginx-gunicorn/gunicorn/systemd/gunicorn.service /etc/systemd/system/gunicorn.service
#cp /vagrant/flask-nginx-gunicorn/nginx/opm /etc/nginx/sites-available/opm
# services
#systemctl daemon-reload
#systemctl start gunicorn.service
#ln -s /etc/nginx/sites-available/opm /etc/nginx/sites-enabled/opm
#rm /etc/nginx/sites-enabled/default
#systemctl enable gunicorn.service
#systemctl reload nginx
#cd /home/vagrant/opm && bash ./init_tagger_db.sh
#systemctl stop gunicorn.service
#systemctl start gunicorn.service
