import urllib
import json

def uber_products(lat,lon,uber_server_token):    
    url = 'https://api.uber.com/v1/products?'

    parameters = {
    'server_token': uber_server_token,
    'latitude': lat,
    'longitude': lon,
    }    
    response = urllib.request.Request(url+urllib.parse.urlencode(parameters))
    data = urllib.request.urlopen(response).read()
    return (data)




def uber_estimate(lat,lon,access_token):
    payload=json.dumps({'start_latitude':lat
                        ,'start_longitude':lon
                        ,'end_latitude':40.621772
                        ,'end_longitude': -111.894836
                        }).encode('utf-8')  
    headers={'Authorization':'Bearer '+ access_token
              ,"Content-Type": "application/json"
             ,'Content-Length':len(payload)
             ,'charset':'utf-8'}
    #r=urllib.request.Request('https://6f92acd3.ngrok.io',data=payload,headers=headers)
    r=urllib.request.Request('https://api.uber.com/v1/requests/estimate',data=payload,headers=headers)   
    resp=urllib.request.urlopen(r)   
    print(resp.read())
    #print(resp['access_token'])
