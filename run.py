from flask import Flask
from flask import request
from flask import make_response
from http.client import HTTPResponse
import json
import codecs
import  urllib

app=Flask(__name__)
creds={}

with open('credentials.txt','r') as file:
    for f in file:        
        creds[f.split(',')[0]]=f.split(',')[1]
        
        
token=creds['fb_page_token'] #put the page token from Facebook apps
page_link=creds['page_link'] #eg /fdffdfefre1213
verify_token=creds['fb_verify_token'] #in webhooks

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
                print(m['message'])
                payload = urllib.parse.urlencode({'recipient': {'id': sender}, 'message': {'text': "Hello World"}} ).encode()
                send_text(payload)
            except:
                print(m.keys())
    return make_response("",200)


def send_text(text):          
     r=urllib.request.Request('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token,data=text)
     resp=urllib.request.urlopen(r)


app.run(debug=True)
