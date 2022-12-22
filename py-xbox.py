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
parser_friends.add_argument('action', choices=['list', 'online', 'recents' ])
parser_friends.add_argument('--count', '-c', default=10, help='The maximum count of people to show at once')

parser_messages = subparser.add_parser('messages')
parser_messages.add_argument('action', choices=['list', 'send', 'requests'])

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

#print("Apikey succesfully loaded")

## creating a sesssion
session = requests.session()
session.headers = {
        'x-authorization':apikey
}

## functions
def apiget(url):
    response = session.get(endpoint + url)
    #print(response)
    return json.loads(response.text)
def apipost(url, content):
    response = session.post(endpoint + url, json=content)
    return response.text

def gamertag_for_xuids(xuids_orig):
    xuids_orig = [*set(xuids_orig)]#removing duplicates
    
    xuids = []
    #split the list into chunks of 10
    start = 0
    end = len(xuids_orig)
    step = 10
    for i in range(start, end, step):
        x = i
        xuids.append(xuids_orig[x:x+step])

    gamertag_xuids = []

    for part in xuids:
        str_xuids = ','.join(part).replace(',','%2C')
        infos = apiget('/api/v2/account/' + str_xuids)
        for person in infos['people']:
            gamertag_xuids.append({'xuid' : person['xuid'] , 'name' : person['displayName']})

    return list(gamertag_xuids)

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
        
        try:
            count = int(args['count'])
        except Exception:
            count = 10

        for item in timemet_person_arr[:count]:
            person = item['person']
            print(f'{person["displayName"]} : {person["recentPlayer"]["text"]}')

elif action=='messages':
    subaction = args['action']

    if subaction == 'list':
        msg_json = apiget('/api/v2/conversations')
        conversations = msg_json['primary']['conversations']
        
        ## we have to get all xuids to get the gamertag of each gamertag
        xuids = []
        for convers in conversations:
            for participant in convers['participants']:
                xuids.append(participant)

        xuid_name_dict = gamertag_for_xuids(xuids)
        
        for convers in conversations:
            message = convers['lastMessage']['contentPayload']['content']['parts'][0]['text']
            time = dateutil.parser.isoparse(convers['timestamp'])
            participants = []

            for participant in convers['participants']:
                for part in xuid_name_dict:
                    if participant == part['xuid']:
                        participants.append(part['name'])

            print(f'{time.ctime()} {",".join(participants)} : {message}')
    if subaction == 'requests':
        msg_json = apiget('/api/v2/conversations/requests')
        conversations = msg_json['conversations']
        
        ## we have to get all xuids to get the gamertag of each gamertag
        xuids = []
        for convers in conversations:
            for participant in convers['participants']:
                xuids.append(participant)

        xuid_name_dict = gamertag_for_xuids(xuids)
        #print(xuid_name_dict)

        for convers in conversations:
            message = convers['lastMessage']['contentPayload']['content']['parts'][0]['text']
            time = dateutil.parser.isoparse(convers['timestamp'])
            participants = []
            for participant in convers['participants']:
                for part in xuid_name_dict:
                    if participant == part['xuid']:
                        participants.append(part['name'])
            print(f'{time.ctime()} {",".join(participants)} : {message}')
