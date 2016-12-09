#!/usr/bin/env python3

import time
import requests
import json
import ids
from random import randint
import sys
import os

## Ojbects: name -> (mass_gain, humor_gain)
## 
objects = dict()
objects['Mushroom'] = (+20, -20)
objects['Kicker']   = (+25, +25)
objects['Cookie']   = (+15, +0)
objects['Bra']      = (+0,  +50)
objects['Kitty']    = (+0,  +0)
objects['Pants']    = (+0,  +0)
objects['Eye']      = (+0,  +0)
objects['Lord']     = (+0,  +0)

objects_char = dict()
objects_char['Mushroom'] = '0';
objects_char['Kicker']   = '1';
objects_char['Cookie']   = '2';
objects_char['Bra']      = '3';
objects_char['Kitty']    = '4';
objects_char['Pants']    = '5';
objects_char['Eye']      = '6';
objects_char['Lord']     = '7';

def get_game_state_url():
    return "https://shrek.getmobileup.com/api/game/state"

def get_game_action_url():
    return "https://shrek.getmobileup.com/api/game/action"

def get_headers():
    return {'Content-type': 'Application/json'}

def get_game_state():
    request = dict()
    request['gameId']  = ids.get_game_id()
    request['droidId'] = ids.get_droid_id()
    request_json = json.dumps(request)
    response = requests.post(get_game_state_url(), headers=get_headers(), data=request_json)
    return json.loads(response.text)

def put_game_actions(currentTurn, actions):
    request = dict()
    request['gameId']      = ids.get_game_id()
    request['droidId']     = ids.get_droid_id()
    request['currentTurn'] = currentTurn
    request['actions']     = actions
    request_json = json.dumps(request)
    response = requests.post(get_game_action_url(), headers=get_headers(), data=request_json)
    return json.loads(response.text)

def print_state2array(state):
    for i in range(5):
        for j in range(5):
            item = state['map'][i * 5 + j]
            if item['isBorder'] == True:
                sys.stdout.write("#")
            elif 'object' in item:
                sys.stdout.write(objects_char[item['object']['name']])
            elif item['gamer'] != None:
                if item['gamer'] == "Shrekosaur":
                    sys.stdout.write("X")
                else:
                    sys.stdout.write("g")
            else:
                sys.stdout.write("_")
        print("")    
    print("-----------------------")        

def get_direction(state):
    index = randint(0, 8)
    return "goto" + str(index + 1)

def get_actions(state):
    actions = list()
    direction = get_direction(state)
    actions.insert(0, direction)
    return actions
    
if __name__ == "__main__":
    while True:
        state = get_game_state()
        if state['yourTurn'] == False:
            time.sleep(0.5)
            continue

        actions  = get_actions(state)
        response = put_game_actions(state['currentTurn'], actions)
        print_state2array(state)

        

