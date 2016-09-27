import urllib

def uber_estimates(lat,lon,uber_server_token):    
    url = 'https://api.uber.com/v1/products?'

    parameters = {
    'server_token': uber_server_token,
    'latitude': lat,
    'longitude': lon,
    }    
    response = urllib.request.Request(url+urllib.parse.urlencode(parameters))
    data = urllib.request.urlopen(response).read()
    return (data)
