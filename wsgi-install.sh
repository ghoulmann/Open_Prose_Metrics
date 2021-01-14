cd /vagrant/
unzip /vagrant/4.7.1.zip
cd mod_wsgi-4.7.1/
./configure --with-python=/usr/bin/python3.7
make
make install

#cp /usr/lib/apache2/modules/mod_wsgi.so /etc/apache2/modules/
chmod 644 /usr/lib/apache2/modules/mod_wsgi.so
systemctl reload apache2
