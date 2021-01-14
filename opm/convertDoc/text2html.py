# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

def htmlify(ucodetext):
    return ucodetext.encode('ascii', 'xmlcharrefreplace')
