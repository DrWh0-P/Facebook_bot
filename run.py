from flask import Flask
from flask import request
from flask import make_response
from http.client import HTTPResponse
import json
import codecs
import  urllib

app=Flask(__name__)
token=<token>
reader=codecs.getreader('utf-8')
@app.route('/fdffdfefre12123',methods=['GET'])
def home():    
    if request.args['hub.verify_token'] == 'ente#devame1':         
        return make_response(request.args['hub.challenge'])

@app.route('/fdffdfefre12123',methods=['POST'])
def echo():  
    body=request.get_json()
    #rint(body['entry'])    
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
