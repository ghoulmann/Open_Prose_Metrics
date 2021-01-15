import json
import os

class BaseConfig(object):
    'Base config class'
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    TESTING = False
    #TMP_DIR = 'tmp'
    #UPLOAD_FOLDER = TMP_DIR
    SHELVE_FILENAME = os.path.join(basedir, 'shelve.db')
    SHELVE_LOCKFILE = os.path.join(basedir,'shelve.db.lock')
    SESSION_TYPE = 'null'
    SESSION_PERMANENT = False
    SESSION_COOKIE_NAME = 'session'
    DARMODE = True
    if os.path.isfile('instance/key.txt'):
        try:
            with open('instance/key.txt') as kf:
                 SECRET_KEY = kf.read()
        except:
            SECRET_KEY = os.urandom(12).hex()
    else:
        SECRET_KEY = os.urandom(12).hex()
class ProductionConfig(BaseConfig):
    'Production specific config'
    DEBUG = False
    #TTS_DIR = "/static/audio/"
    UPLOAD_FOLDER = '/var/www/html/extraeyes/app/tmp/' # wsgi
    SITEMAP_URL_SCHEME = 'https'
    #UPLOAD_FOLDER = TMP_DIR
    #USE_X_SENDFILE = True
    # MAX_CONTENT_LENGTH = 32 * 4096
    SITEMAP_URL_SCHEME = 'https'
class DevelopmentConfig(BaseConfig):
    'Development environment specific config'
    DEBUG = True
    TESTING = True
    FLASK_ENV = "development"
    TTS_DIR = "static/audio/"
