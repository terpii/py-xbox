import requests
import argparse
import json
import sys
import datetime
import dateutil.parser

endpoint = 'https://xbl.io'




# argparse 
parser = argparse.ArgumentParser(
        prog= 'pyxbox',
        description='A command line interface for interacting with xbox')

subparser = parser.add_subparsers(title='action', required=True, 
                                  help='action to execute')

parser_help = subparser.add_parser('help')

parser_friends = subparser.add_parser('friends')
parser_friends.add_argument('action', choices=['list', 'online', 'recents'])

args = vars(parser.parse_args())

#parser_messages = subparser.add_parser('messages')




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

action = sys.argv[1]




if action=='help':
    parser.print_help()
elif action=='friends':
    subaction = args['action'] 
    
    if subaction == 'list':
        friends_json = apiget('/api/v2/friends') 
        for person in friends_json['people']:
            print(f"{person['gamertag']} : {person['presenceText']}")
    
    if subaction == 'online': 
        friends_json = apiget('/api/v2/friends') 
        for person in friends_json['people']:
            if person['presenceState'] == 'Online':
                print(f"{person['gamertag']} : {person['presenceText']}")
    
    if subaction == 'recents':
        recents_json = apiget('/api/v2/recent-players')

        timemet_person_arr = []

        for person in recents_json['people']:
            time_str = person['recentPlayer']['titles'][0]['lastPlayedWithDateTime']
            date = dateutil.parser.isoparse(time_str)

            timemet_person_arr.append({'person':person,'time':date})
        
        timemet_person_arr.sort(key = lambda x : x['time'])
        timemet_person_arr.reverse()

        for item in timemet_person_arr[:15]:
            person = item['person']
            print(f'{person["displayName"]} : {person["recentPlayer"]["text"]}')
