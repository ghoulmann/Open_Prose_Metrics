# -*- coding: utf-8 -*-
""" Routes for essay analysis interface"""

import flask
import json
import logging
import os
import traceback
#import urllib3.request, urllib3.error, urllib3.parse,
import urllib
from html.parser import HTMLParser
from logging.handlers import RotatingFileHandler
from random import randint
from time import strftime
import werkzeug
from bs4 import BeautifulSoup
#from BeautifulSoup import BeautifulSoup as BS
from flask import Flask, abort, flash, jsonify, make_response, redirect, render_template, send_from_directory, request, session, url_for
from flask_bootstrap import Bootstrap, WebCDN, bootstrap_find_resource
from flask_nav import Nav
from flask_nav.elements import *
import flask_shelve
from flask_shelve import get_shelve
from werkzeug.utils import secure_filename
from input import read_document, read_text
from flask_sitemap import Sitemap
from tts.tts import TTS
from unidecode import unidecode_expect_nonascii
from presentation.presentation import FrontEnd
from datetime import datetime
import shelve
app = Flask(__name__, static_url_path='/static')
if "/var/www/" in os.path.abspath(__file__):
     app.config.from_object('configuration.ProductionConfig')
elif "/var/www/" in os.path.abspath(__file__) or os.environ.get('FLASK_ENV') == "production":
     app.config.from_object('configuration.ProductionConfig')
else:
    app.config.from_object('configuration.DevelopmentConfig')
#app.name = "extraeyes"

logger = logging.getLogger(__name__)
handler = RotatingFileHandler('/var/log/extraeyes/app.log', maxBytes=10000, backupCount=3)
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)
log.addHandler(handler)
logging.getLogger('werkzeug')
# maxBytes to small number, in order to demonstrate the generation of multiple log files (backupCount).

logger.addHandler(handler)
# getLogger(__name__):   decorators loggers to file + werkzeug loggers to stdout
# getLogger('werkzeug'): decorators loggers to file + nothing to stdout
"""
Upload Folder

Defined differently for difference scenarios:

* pythonanywhere
* wsgi
* flask dev
"""

#UPLOAD_FOLDER = 'tmp' # local dev
# UPLOAD_FOLDER = '/tmp' # pythonanywhere
UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "/tmp/" #flask alone
#UPLOAD_FOLDER = '/var/www/html/extraeyes/app/tmp/' # wsgi
AUDIO_DIR = os.path.dirname(os.path.realpath(__file__)) + "/static/audio/"

ALLOWED_EXTENSIONS = set(['txt', 'docx', 'odt', 'pdf', 'doc', 'rtf', 'txt'])
topbar = Navbar('',
    #Text("Open Prose Metrics"),
    
    View('Open Prose Metrics', 'intro'),
    View('Upload', 'upload_file'),
    View('Paste', 'paste'),
    View('URL', 'scrape_url'),
    View('Example', 'show_example'),
    Subgroup('External Resources',
             Link('Lard', 'http://proftgreene.pbworks.com/w/file/fetch/50167777/Richard%20Lanhams%20Paramedic%20Method%20of%20Revision.pdf'),
             Link('Lard Factor', 'http://faculty.winthrop.edu/kosterj/WRIT465/slide%20shows/lardoutline_files/frame.htm'),
             Link('Readability',
                  'http://www.analyzemywriting.com/readability_indices.html'),
             Link('Revision Strategies', 'http://greyfiti.wikidot.com/sdg:gmeth-ref-guidelines-substantive-revision'),
             Link('Atrocity of Adverbs', 'https://www.brainpickings.org/2013/03/13/stephen-king-on-adverbs/'),
             Link('Timeless Advice on Writing', 'https://www.brainpickings.org/2013/05/03/advice-on-writing/'),
             Link('Style Checks','http://proselint.com/checks/'),
             Link('Paramedic Method', 'https://owl.purdue.edu/owl/general_writing/academic_writing/paramedic_method.html'),
             Link('E-Prime', 'https://www.nobeliefs.com/eprime.htm'),
             ),
)

nav = Nav()
nav.register_element('top', topbar)
#app = Flask(__name__)

if "/var/www/" in os.path.abspath(__file__):
    try:
        app.config.from_object('configuration.ProductionConfig')
    except:
        app.config.from_object('configuration.DevelopmentConfig')
elif "/var/www/" in os.path.abspath(__file__) or os.environ.get('FLASK_ENV') == "production":
    app.config.from_object('configuration.ProductionConfig')
else:
    app.config.from_object('configuration.DevelopmentConfig')

ext = Sitemap(app=app)
#app.config['SESSION_TYPE'] = 'filesystem'
#app.config['SHELVE_FILENAME'] = 'shelve.db'
#app.config['SHELVE_LOCKFILE'] = 'shelve.db.lock'
#app.config['SESSION_TYPE'] = 'null'
#app.config['SESSION_PERMANENT'] = 'False'
Bootstrap(app)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 32 * 4096 #12/19/2018
app.extensions['bootstrap']['cdns']['slate'] = WebCDN("https://cdnjs.cloudflare.com/ajax/libs/bootswatch/3.3.7/slate/")
app.extensions['bootstrap']['cdns']['cyborg'] = WebCDN("https://stackpath.bootstrapcdn.com/bootswatch/3.3.7/cyborg/")
nav.init_app(app)
flask_shelve.init_app(app)
_samples=[]



# Views and other stuff

def allowed_file(filename):
    """
    Make sure filetype has allowed extension.

    * docx: most reliable
    * odt: through textract (spaces between words disappear, as do
        apostrophes)
    * txt: works fine
    """

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/feedback/<datetime>/shelve/', methods=['GET', 'POST'])
def save_to_db(datetime):
    if Doc.timestamp:
        key = Doc.timestamp
        db = get_shelve('c')
        db[Doc.time_stamp] = Doc
        
        #if "/shelve/" in request.path:
         #   status = """<span style="padding:15px; font-size:25px; vertical-align:top" title="save" class="glyphicon glyphicon-floppy-disk hidden-print"></span>"""
        #else:
        status = """<span style="vertical-align:top" title="saved" class="glyphicon glyphicon-floppy-saved hidden-print"></span>"""
        #if "shelve" in request.path:
        #    status = ' class=\"glyphicon glyphicon-floppy-disk hidden-print\" '
        #else:
        #    status = ' class=\"glyphicon glyphicon-floppy-saved hidden-print\" '
        return render_template('new_results.html', object=Doc, icon=status)
@app.route('/example/')
def show_example():

    # #if request.method == 'GET':
    # Doc = read_document.Sample('/util/essay_samples/12Grade-informationExplanatory.txt', 'student', 'no')
    # return redirect(url_for('feedback', timestamp = Doc.timestamp))
    # #else:
    #  #   return redirect(url_for('intro'))
    db = get_shelve('c')
    Doc = db['example']
    return render_template('new_results.html', object=Doc)
@app.route('/admin/shelve/')
def shelve():
    db = get_shelve('c')
    
    keys = list(db.keys())
    return render_template('keys.html', keys = keys)
    
@app.route('/admin/feedback/<key>', methods=['GET'])
def show_record(key):

    # #if request.method == 'GET':
    # Doc = read_document.Sample('/util/essay_samples/12Grade-informationExplanatory.txt', 'student', 'no')
    # return redirect(url_for('feedback', timestamp = Doc.timestamp))
    # #else:
    #  #   return redirect(url_for('intro'))
    
    db = get_shelve('c')
    Doc = db[key]
    return render_template('new_results.html', object=Doc)



@app.route('/clear')
def clearRawText(): 
    Doc = read_document.Sample("A certain change in the emphasis on having and being is apparent in the growing use of nouns and the decreasing use of verbs in Western languages in the past few centuries. A noun is the proper denotation for a thing. I can say that I have things: for instance that I have a table, a house, a book, a car. \n The proper denotation for an activity, a process, is a verb: for instance I am, I love, I desire, I hate, etc. Yet ever more frequently an activity is expressed in terms of having; that is, a noun is used instead of a verb. But to express an activity by to have in connection with a noun is an erroneous use of language, because processes and activities cannot be possessed; they can only be experienced.")

    return redirect(url_for('intro'))

"""
def clearSession(instance=Doc):
    '''
    Stop intermittant breaking between upload and parsing, delivering instance.

    Still not clear if this is the remedy.
    '''



    try:
        session.clear()
        print "Session cleared"
    except:
        print "Attempt to clear session failed"
        pass


    try:
        deleteInstance(instance)
        del instance
    except:
        pass

    if Doc:
        print "The instance of Sample has not been properly destroyed."
    else:
        print "There is not Sample instance called 'Doc'"

    return redirect(url_for('intro'))
"""


@app.route('/')
def intro():
    return render_template('index.html')

# @app.route('/about')
# def about():
#     """Flask route to the about page."""
#     return render_template('about.html')
@ext.register_generator
def index():
    # Not needed if you set SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS=True
    yield 'intro', {}
    yield 'paste', {}
    yield 'upload_file', {}
    yield 'scrape_url', {}

@app.route('/paste/', methods=['GET', 'POST'])
def paste():
    #num1 = randint(1, 10)
    #num2 = randint(1, 10)
    if request.method == 'POST':
        if request.form['email_add']:
            return render_template('404.html')
        #if (request.form['userSolution'] != request.form['sum']):
        #    return redirect(request.url)
        result = request.form
        if 'plaintext' not in result:
            flash('No text submitted') # does not work yet
            return redirect(request.url)
        if 'author' not in result:
            return redirect(request.url)
        prose = unidecode_expect_nonascii(result['plaintext'])
        apis = result['apis']
        author = result['author']
        administrator = result['administrator']
        admin_notes = result['notes']
        global Doc

        Doc = read_document.Sample(prose, author, apis)
        Doc.administrator = administrator
        Doc.admin_notes = admin_notes
        Doc.timestamp = datetime.now()
        return redirect(url_for('feedback', timestamp=Doc.timestamp))
    return render_template('paste.html')

@app.route('/url/', methods=['GET', 'POST'])
def scrape_url():
    #num1 = randint(1, 10)
    #num2 = randint(1, 10)
    if request.method == 'POST':
        if request.form['email_add']:
            return render_template('404.html')
        #if (request.form['userSolution'] != request.form['sum']):
        #    return redirect(request.url)
        result = request.form
        if 'plaintext' not in result:
            return redirect(request.url)
        #if 'author' not in result:
        #    author = ""
        url = result['plaintext']
        target = urllib.request.Request(url)
        target.add_header('Accept-Encoding', 'utf-8')
        target.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
        response = urllib.request.urlopen(target)
        #soup = BS(response.read().decode('utf-8'), convertEntities=BS.HTML_ENTITIES)
            #soup = BS(response.read().decode('utf-8', 'ignore'), convertEntities=BS.HTML_ENTITIES)
        soup = BeautifulSoup(response, 'html.parser')
        # except urllib2.HTTPError, e:
        #     print('We failed with error code %s' % e.code)
        #     if e.code == 404:
        #         render_template('404.html')
        #     elif e.code == 403:
        #         render_template('403.html')
        #     else:
        #         pass
            #paragraphs = ""
        #for s in soup.findAll('br'):
        #    paragraphs += s.get_text(separator=" ", strip=True)
        paragraphs = soup.findAll('p')
            #title = soup.find('title')
        title = soup.title.string
            #h = HTMLParser()
            #paragraphs = h.unescape(paragraphs)
            #title = title.getText()
            #title = h.unescape(title)
        plaintext = ""
        for p in paragraphs:
            plaintext += p.text + "\n\n"
            #plaintext += p.getText() + '\n\n'
            #plaintext += p.getText(" ") + '\n\n'

        prose = unidecode_expect_nonascii(plaintext)
        #prose = paragraphs
        apis = result['apis']
        author = result['author']
        administrator = result['administrator']
        admin_notes = result['notes']

        global Doc

        Doc = read_document.Sample(prose, author, apis)
        Doc.administrator = administrator
        Doc.admin_notes = admin_notes
        if title:
            Doc.title = title
        else:
            Doc.title = url
        if Doc:
            return redirect(url_for('feedback', timestamp=Doc.title))
        else:
            return render_template('url.html')
    else:
        return render_template('url.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    Upload file to UPLOAD_FOLDER from form on upload template.

    After upload, create instance, then redirect to results.

    .. todo::
        * add some kind of indicator that the wait is expected
        * make flash work

    Return:
        Redirect to feedback template on successful POST.
    """
    
    #num1 = randint(1, 10)
    #num2 = randint(1, 10)
    if request.method == 'POST':
        # use on each form page

        if request.form['email_add']:
            return render_template('404.html')
        #if (request.form['userSolution'] != request.form['sum']):
        #    return redirect(request.url)
        if 'file' not in request.files:
            flash('No file part') # does not work yet
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file') # does not work
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            global Doc

            #time.sleep(3) # no effect on intermittent instance creation
            #Doc = read_document.Sample(UPLOAD_FOLDER + "/" + filename, request.form['author'], request.form['apis'])


            Doc = read_document.Sample(UPLOAD_FOLDER + "/" + filename, request.form['author'], request.form['apis'])

            try:
                Doc.administrator = request.form['administrator']
            except:
                Doc.administrator = "unidentified"
            try:
                Doc.admin_notes = request.form['notes']
            except:
                Doc.admin_notes = "None specified"
            try:
                Doc.description = request.form['description']
            except:
                print("could not set object description attribute from post request field ")

            
            return redirect(url_for('feedback', timestamp=Doc.time_stamp))


    return render_template('upload.html')

@app.route('/feedback/<timestamp>', methods=['GET', 'POST'])
def feedback(timestamp):
    """
    Route to analysis results (of uploaded file)

    On the way, remove the uploaded doc from the defined storage location
    """
    try:
        if Doc:
            print("An instance of Sample exists.")
    except:
        print("No instance.")


    try:

        if Doc.raw_text:
            _samples.append(timestamp)
            for sample in _samples:
                print(sample)
            try:
                if os.path.isfile(Doc.abs_path):
                    os.remove(Doc.abs_path)
                if not os.path.isfile(Doc.abs_path):
                    print("Destroyed tmp file %s." % Doc.abs_path)
            except:
                print("Failed to remove tmp file %s. Please check owner and \
                    permissions" % Doc.abs_path)
                pass
    except:
        pass

    if Doc.raw_text:

        if Doc.text_language != 'en':
            return render_template('400.html')


    if "/shelve/" in request.path:
         status = """<span style="vertical-align:top" class="glyphicon glyphicon-floppy-saved hidden-print"></span>"""
    else:
         status = """<span style="vertical-align:top" class="glyphicon glyphicon-floppy-disk hidden-print"></span>"""

    return render_template('new_results.html', object=Doc, icon=status)


    #except:
    #    return render_template('404.html')

def get_audio():
    timestamp = Doc.time_stamp
    if Doc.raw_text:

        try:
            saveto = AUDIO_DIR + ("%s.mp3" % timestamp)
            Doc.tts = TTS(Doc.raw_text, saveto)
            return Doc.tts.mp3Confirm()
        except FileNotFoundError:
            print("Doc.tts.mp3Confirm() did not succeed.")
        


        #Doc.tts = TTS(Doc.raw_text, "/var/www/html/extraeyes/app/static/audio/%s.mp3" % timestamp)
        #return Doc.tts.mp3Confirm()
    else:
        return render_template('400.html')


@app.route('/feedback/<timestamp>/tts/', methods=['GET'])
@app.route('/feedback/<timestamp>/TTS/', methods=['GET'])
@app.route('/feedback/<timestamp>/proofread/', methods=['GET'])
def proofread(timestamp):
    """
    Show page with raw_text and rendering of TTS

    return proofread-w-tts.HTMLParser template
    """
    timestamp = Doc.time_stamp
    Doc.tts = get_audio()
    Doc.tts_basename = os.path.basename(Doc.tts)
    return render_template('proofread-w-tts.html', object=Doc, timestamp=timestamp)



@app.route('/content')
def content():
    """
    Show full text of the raw_text of the instance from upload.

    (object.raw_text)
    """
    return render_template('content.html', object=Doc)

@app.route('/usage')
def usage():
    """ Show documentation. """
    return render_template('usage.html')

@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_internal_server_error(e):
    """ Error handler that appears to be working """
    return render_template('internal.html'), 500


@app.route('/404')
def page_not_found():
    return render_template('404.html')
#@app.route('/json')
#def json_out():
#    return jsonify(object.api_report)


"""
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
"""

@app.route('/docs_api', methods=['POST', 'GET'])
def docs_api():
    if request.method == "POST":
        # form = '''<form method="post">
        #     author: <input type="text" name="author" required><br>
        #     apis: <input type="boolean" name="external"><br>
        #     plaintext: <input type="textarea" name="body" required><br>
        #     <input type="submit" value="Submit"><br>
        #     </form>'''
        # result = request.form
        if (request):
            result = request.get_json()

        # if 'plaintext' not in result:
        #     flash('No text submitted') # does not work yet
        #     return abort(400)
        # if 'author' not in result:
        #     return abort(400)
        # if 'apis' not in result:
        #     result['apis'] = False
        #prose = unidecode_expect_nonascii(result['plaintext'])

            author = result['author']
            prose = result['plaintext']
            apis = result['apis']
        # prose = unidecode_expect_nonascii(content['plaintext'])
        #apis = result['apis']

        #author = result['author']

            global Doc
            Doc = read_document.Sample(prose, author, apis)
        #time.sleep(3) # doesn't resolve intemittant breaking
        #try:
            data = Doc.toDict()
        #except:
        #    return render_template('500.html'), 500
            return jsonify(data), 200
    return render_template('401.html'), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":

    #app.run
    logger = logging.getLogger(__name__)
    handler = RotatingFileHandler('log/app.log', maxBytes=10000, backupCount=3)
    #log = logging.getLogger('werkzeug')
    log.setLevel(logging.INFO)
    log.addHandler(handler)
    #logging.getLogger('werkzeug')
    # maxBytes to small number, in order to demonstrate the generation of multiple $

    logger.addHandler(handler)
    # getLogger(__name__):   decorators loggers to file + werkzeug loggers to stdout

    app.run()


