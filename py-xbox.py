import requests
import argparse
import json
import sys

endpoint = 'https://xbl.io'

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
session = requests.session()
session.headers = {
        'x-authorization':apikey
}

## functions
def apiget(url):
    response = session.get(endpoint + url)
    return json.loads(response.text)
def apipost(url, content):
    response = session.post(endpoint + url, json=content)
    return response.text

actions = ['help','list-friends', 'list-recents']

# argparse 
parser = argparse.ArgumentParser(
        prog= 'pyxbox',
        description='A command line interface for interacting with xbox')

parser.add_argument('action', default='help',
                    const='help',
                    help='the action you want to execute',
                    nargs='?',
                    choices=actions)
args = vars(parser.parse_args())



