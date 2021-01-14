# shelve.db temporarily unavailable

Remedy as so:

```python
from threading import Lock
import shelve

mutex = Lock()

mutex.acquire()
db = shelve.open(db_name)
# write to db
db.close()
mutex.release()
```

# gunicorn log directives

```bash
# Flask, OPM, Gunicorn Service

[Unit]
Description=Gunicorn instance to serve Open Prose Metrics via Gunicorn and Flask
After=network.target

[Service]
User=vagrant
Group=www-data
WorkingDirectory=/home/vagrant/opm
ExecStart=/usr/local/bin/gunicorn --access-logfile /var/log/extraeyes/gunicorn-access.log --error-logfile /var/log/extraeyes/gunicorn-error.log --workers 3 --bind unix:/tmp/gunicorn.sock -m 007 wsgi:app


[Install]
WantedBy=multi-user.target
```

# nginx proxy timeout

Add to nginx.conf under http json

```nginx
http {

    ##
    # Basic Settings
    ##
    proxy_connect_timeout       1600;
    proxy_send_timeout          1600;
    proxy_read_timeout          1600;
    send_timeout                1600;
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    ...
}
```

# Install Python3.7 on Ubuntu 18.04

For me, I had to install pip for 3.6 first

```
sudo apt install python3-pip
```

now you can install python 3.7

```
sudo apt install python3.7
```

and then I could install pip for 3.7

```
python3.7 -m pip install pip
```

and as a bonus, to install other modules just preface with

```
python3.7 -m pip install <module>
```

## Get pip

This works for me.

    `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`

Then this command with sudo:

    `python3.7 get-pip.py`

Based on [this instruction](https://pip.pypa.io/en/stable/installing/).
