#!/usr/bin/env python3

import time
import requests
import json

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
    return "https://shrek.getmobileup.com/api/game/state"

def get_game_id():
    return "b33b8a50-bddb-11e6-9911-6532d6ea992e-6c1f1dcb-1bd9-4991-9ed4-bbed1a5ca3ba"

def get_droid_id():
    return "5f4c0d90-bd4d-11e6-b3e3-0911bb93107b-93cf40d2-10d9-4df7-88a8-517de1d89dd2"

def get_headers():
    return {'Content-type': 'Application/json'}

def get_game_state():
    request = dict()
    request['gameId']  = get_game_id()
    request['droidId'] = get_droid_id()
    request_json = json.dumps(request)
    response = requests.post(get_game_state_url(), headers=get_headers(), data=request_json)
    return json.loads(response.text)

def put_game_actions(currentTurn, actions):
    request = dict()
    request['gameId']    = get_game_id()
    request['droidId']   = get_droid_id()
    request['currentId'] = currentTurn
    request['actions']   = actions
    request_json = json.dumps(request)
    response = requests.post(get_game_action_url(), headers=get_headers(), data=request_json)
    return json.loads(response.text)

def get_actions(state):
    return ["goto1"]
    
if __name__ == "__main__":
    while True:
        state = get_game_state()
        print(state['yourTurn'], state['currentTurn'])
        
        if state['yourTurn'] == False:
            time.sleep(0.5)
            continue

        actions  = get_actions(state)
        response = put_game_actions(state['currentTurn'], actions)
        print(response)
        

