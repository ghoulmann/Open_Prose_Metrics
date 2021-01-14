# Open Prose Metrics: with Apache2, mod_wsgi, virtualenv from source

#####
# Environment:
# Ubuntu 18.04
# Apache2
# mod_wsgi installed from source
# Virtualenv Python 3.7.5
####

############################################################
# Install Options
############################################################

INSTALLER_DIR = $PWD
TARGET_DIR = /var/www/html/open-prose-metrics
APP_OWNER = vagrant
APP_GROUP = www-data
LOG_DIR = /var/log/opm
VENV = /var/www/html/open-prose-metrics/virtualenv
NER_DIR = /usr/share/stanfor-ner
NLTK_DATA_DIR = /usr/share/nltk_data
