

#params = DocumentParameters()
#params['contentString'] = plaintext_string
#params['language'] = "eng"
#params['title'] = 'sample text'

#def rosette_client(key, url, API):
#    client = API(user_key=key, alt_url=url)
#    return client

def parameters(text, DocumentParameters, language='engl'):
    params = DocumentParameters()
    params["content"] = text
    params["language"] = language
    return params

def rosette_request(client, call, params):
    request = client.call[params]
    return request
