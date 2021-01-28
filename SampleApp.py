import logging
import requests 
import json
import base64


logging.basicConfig(format='%(asctime)s [%(levelname)s] : %(message)s',level=logging.DEBUG)

# https://pro.coinmarketcap.com/account
COIN_API_KEY = 'ca4addc3-2e2a-4c2a-9a15-c8f9c4c929da'

def fetching_coin_market_cap():

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
  'symbol':'BTC,ETH,LTC,ADA,XLM,POL,DOGE',
  'convert':'EUR'
    }
    headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': COIN_API_KEY,
    }
    r = requests.get(url,headers=headers, params=parameters)
    assert r.status_code == 200 
    return r.json()

def create_dg_note(text, name, dbid, token):
    form_data = {
            'datafile':(name ,text,'application/octet-stream'),
            'parameter':
            ('',json.dumps({
                'docName':name,
                'filename':name,
                'format':'TXT',
                'docTypeId': 0,
                'docClass': {'value':'FILE', 'flag':0},
                'isVersionable':False
            }),'application/json')
          }
    query = {'isSapCompliant' : False}
    header = {'X-ARCHIVETOKEN':token}  
    r = requests.post(f'http://dataglobal-cs/RESTfulAPI/csrest/v1.1/dept/{dbid}/docs/', headers=header,files=form_data, params=query)
    assert r.status_code == 201
    return r.json()

def create_mark_down(data):
    mark_down = f"# Crypto Markt {data['status']['timestamp']}\n"
    mark_down+= create_png_md_imge('./dogecoin.png')+"\n\n"
    mark_down+="|Symbol|Name|EUR|\n"
    mark_down+="|------|----|---|\n"
    
    
    for name,info in data['data'].items():
        logging.info(f"fetching {info['name']} {name} {info['quote']['EUR']['price']}")
        mark_down += f"|{name}|{info['name']}|{info['quote']['EUR']['price']}|\n"
    return mark_down

def create_png_md_imge(filename):
  assert filename.endswith('png')
  with open (filename,'rb') as f:
    
    return f"![icon](data:image/png;base64,{base64.b64encode(f.read()).decode('UTF-8')})"

def login(user, pwd):

  headers = { 'X-USERNAME':user, 'X-PASSWORD':pwd}
  r = requests.get('http://dataglobal-cs/RESTfulAPI/csrest/v1.1/auth/logon?applClass=Common&progId=Standard',
  headers=headers)
  assert r.status_code == 200

  return r.headers['X-ARCHIVETOKEN']


if __name__ == "__main__":
    token =  login("Administrator","Data230Global")
    logging.info(f"login token:{token}")
 
    #data=fetching_coin_market_cap()
    #md = create_mark_down(data)

    #logging.info(create_dg_note(md,"crypto.txt",1571768983,token))

    
   