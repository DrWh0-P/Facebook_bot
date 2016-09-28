from flask import Flask
from flask import request
from flask import make_response
from http.client import HTTPResponse
import json
import codecs
import  urllib
import re
from uber import uber_estimates

app=Flask(__name__)
creds={}

#store credentials in a file 
with open('credentials.txt','r') as file:
    for f in file:        
        creds[f.split(',')[0]]=f.split(',')[1].strip('\n')
        
        
token=creds['fb_page_token'] #put the page token from Facebook apps
page_link=creds['page_link'] #eg fdffdfefre1213
verify_token=creds['fb_verify_token'] #webhook
uber_server_token=creds['uber_server_token']
uber_client_id=creds['uber_client_id']
uber_client_secret=creds['uber_client_secret']

@app.route(page_link,methods=['GET'])
def home():    
    if request.args['hub.verify_token'] == verify_token :         
        return make_response(request.args['hub.challenge'])
    
@app.route(page_link,methods=['POST'])
def echo():  
    body=request.get_json()      
    for e in body['entry']:        
        for m in e['messaging']:
            sender=m['sender']['id']            
            try:
                if 'text' in m['message']:
                    if re.match('uber',m['message']['text']) is not None:
                        send_text(sender,"what is your current location")
                    elif re.match('how long',m['message']['text']) is not None:
                        text="https://login.uber.com/oauth/v2/authorize?client_id={}&response_type=code".format(uber_client_id)
                        send_text(sender,text)
                    else:                                    
                        send_text(sender,"How may I help you")
                elif ('attachments' in m['message']) :                    
                    lat=m['message']['attachments'][0]['payload']['coordinates']['lat']
                    lon=m['message']['attachments'][0]['payload']['coordinates']['long']
                    data=json.loads(uber_estimates(lat,lon,uber_server_token).decode('utf-8'))
                    
                    for p in data['products']:
                        text=text+","+p['display_name']
                    send_text(sender,text)
            except:
                print("invalid message")
                                   
                   
    return make_response("",200)

@app.route('/submit')
def submit():
    code=request.args['code']
    params={'client_secret':uber_client_secret
            ,'client_id':uber_client_id
            ,'grant_type':'authorization_code'
            ,'redirect_uri':'http://localhost:5000/submit'
            ,'code':code}
    payload=urllib.parse.urlencode(params).encode()
    r=urllib.request.Request('https://login.uber.com/oauth/v2/token',data=payload)
    resp=json.loads(urllib.request.urlopen(r).read().decode('utf-8'))
    print(resp['access_token'])
    return make_response("",200)

def send_text(sender,text):    
     payload = urllib.parse.urlencode({'recipient': {'id': sender}, 'message': {'text': text}} ).encode()
     r=urllib.request.Request('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token,data=payload)
     resp=urllib.request.urlopen(r)


app.run(debug=True)
