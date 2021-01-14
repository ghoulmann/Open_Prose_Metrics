try: 
    from googlesearch.googlesearch import GoogleSearch 
except ImportError:  
    print("googlesearch module is broken becuase of urllib2")
from ddg3 import query as duckducksearch

def google_search(search_query):
    query = search_query
    results = []
    for url in GoogleSearch().search(query, lang='en', num=4, stop=5, pause=2):
        results.append(url.get_text())
    return results

"""returns dict"""
def definition(search_term):
    results = duckducksearch(search_term)
    return results.abstract.text
