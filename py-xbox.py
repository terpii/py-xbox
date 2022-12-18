import requests
import argparse


apikey = ''
## read the api key
try:
    with open('api-key') as f:
        apikey = f.readline()
except:
    print("No api-key found\nPlease paste your apikey into a file name 'api-key'")
    exit(1)

# api key clean ups
apikey = apikey.replace('\n','')
if len(apikey) < 5:
    print('apikey is either missing or invalid, please paste your apikey into the api-key file')
    exit(1)

print("Apikey succesfully loaded")

## creating a sesssion
global session = requests.session()
session.headers. = {
        'x-authorization':apikey
}


