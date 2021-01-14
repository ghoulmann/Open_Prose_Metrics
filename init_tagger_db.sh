#!/bin/bash -ex
python3.7 postagger.py
python3.7 seed_database.py
chown vagrant:www-data tagger.pkl
chown vagrant:www-data shelve.db
