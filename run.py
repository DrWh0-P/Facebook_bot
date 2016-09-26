from flask import Flask
from flask import request
from flask import make_response
from http.client import HTTPResponse
import json
import codecs
import  urllib

app=Flask(__name__)
token=<token> #put the page token from Facebook apps
page_link=<url> #eg /fdffdfefre1213
verify_token=<token> #in webhooks
reader=codecs.getreader('utf-8')
@app.route(page_link,methods=['GET'])
def home():    
    if request.args['hub.verify_token'] == token:         
        return make_response(request.args['hub.challenge'])

@app.route(page_link,methods=['POST'])
def echo():  
    body=request.get_json()      
    for e in body['entry']:        
        for m in e['messaging']:
            try:
                print(m['message']['text'])
                sender=m['sender']['id']                
                payload = urllib.parse.urlencode({'recipient': {'id': sender}, 'message': {'text': "Hello World"}} ).encode()           
                r=urllib.request.Request('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token,data=payload)
                resp=urllib.request.urlopen(r)
            except:
                print(m.keys())
    return make_response("",200)

app.run(debug=True)
