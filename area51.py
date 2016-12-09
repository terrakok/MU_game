#!/usr/bin/env python3

import time
import requests
import json
import ids

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

def state2array(state):
    pass

def get_actions(state):
    return ["goto1"]
    
if __name__ == "__main__":
    while True:
        state = get_game_state()
        state2array(state)
        print(state['yourTurn'], state['currentTurn'])
        
        if state['yourTurn'] == False:
            time.sleep(0.5)
            continue

        print("Perform action")
        actions  = get_actions(state)
        response = put_game_actions(state['currentTurn'], actions)
        print(response)
        

