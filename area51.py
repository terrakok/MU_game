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
    print(request_json)
    response = requests.post(get_game_action_url(), headers=get_headers(), data=request_json)
    return json.loads(response.text)

def print_state2array(state):
    for i in range(5):
        for j in range(5):
            item = state['map'][i * 5 + j]
            if ('gamer' in item) and item['gamer'] != None:
                if item['gamer']['name'] == "Shrekosaur":
                    sys.stdout.write("X")
                else:
                    sys.stdout.write("g")
            elif item['isBorder'] == True:
                sys.stdout.write("#")
            elif 'object' in item:
                sys.stdout.write(objects_char[item['object']['name']])
            else:
                sys.stdout.write("_")
        print("")    
    print("-----------------------")        

current_direction = 3

def get_direction(state):
    global current_direction
    current_direction = int(current_direction + 1) % int(7)
    return current_direction

def is_shreck(index, state):
    item = state['map'][index]
    if ('gamer' in item) and item['gamer'] != None:
        if item['gamer']['name'] == "Shrekosaur":
            return True
    return False

def safe_cell(index, state):
    index_row = int(index / 5)
    index_col = int(index % 5)
    for i in range(index_row - 1, index_row + 2):
        for j in range(index_col - 1, index_col + 2):
              if is_shreck(i * 5 + j, state):
                return False
    return True

def is_free(index, state):
    item = state['map'][index]
    if ('gamer' in item) and item['gamer'] != None:
        return False
    return True

def free_cell(index, state):
    # index_row = int(index / 5)
    # index_col = int(index % 5)
    # for i in range(index_row - 1, index_row + 2):
    #     for j in range(index_col - 1, index_col + 2):
    #           if is_free(i * 5 + j, state):
    #             return False
    # return True
    return is_free(index, state)
    
def is_valid_direction(direction, state):
    indices = [6, 7, 8, 13, 18, 17, 16, 11]
    item    = state['map'][indices[direction]]
    if ('gamer' not in item or item['gamer'] == None) and \
       item['isBorder'] == False and \
       safe_cell(indices[direction], state):
        return True
    return False

def turn_to_safe(state):
    indices = [6, 7, 8, 13, 18, 17, 16, 11]
    for i in range(0, 8):
        print("turn_to_safe:", "(i, indices[i], flag):", i, indices[i], safe_cell(indices[i], state))
    for i in range(0, 8):
        if safe_cell(indices[i], state) and free_cell(indices[i], state):
            return "goto" + str(i + 1)

def is_danger_zone(state):
    return not safe_cell(12, state)

def lookup_danger_zone(state):
    indices = [6, 7, 8, 13, 18, 17, 16, 11]
    for i in range(0, 8):
        if not safe_cell(indices[i], state) and free_cell(indices[i], state):
            return i
    return None

diff2direction = dict()
diff2direction[(-1, -1)] = 1
diff2direction[(-1, +0)] = 2
diff2direction[(-1, +1)] = 3
diff2direction[(+0, +1)] = 4
diff2direction[(+1, +1)] = 5
diff2direction[(+1, +0)] = 6
diff2direction[(+1, -1)] = 7
diff2direction[(+0, -1)] = 8

def lookup_shreck(direction, state):
    indices = [6, 7, 8, 13, 18, 17, 16, 11]
    current_index = indices[direction]
    index_row = int(current_index / 5)
    index_col = int(current_index % 5)
    for i in range(index_row - 1, index_row + 2):
        for j in range(index_col - 1, index_col + 2):
            if is_shreck(i * 5 + j, state):
                return diff2direction[(i - index_row, j - index_col)]
    print("lookup_shreck: ERRORR!!!")
    return -1
                

def object_founded(state):
    item = state['map'][12]
    if 'object' in item:
        if item['object']['name'] == 'Mushroom' or \
           item['object']['name'] == 'Kicker' or \
           item['object']['name'] == 'Cookie' or \
           item['object']['name'] == 'Bra':
            return True
    return False
        
def get_actions(state):
    actions = list()

    if is_danger_zone(state):
        print("get_actions: in danger zone")
        turn_to_safe_str = turn_to_safe(state)
        print(turn_to_safe_str)
        actions.insert(0, turn_to_safe_str)
    else:
        print("get_actions: in safe zone")
        direction = lookup_danger_zone(state)
        if direction == None:
            if object_founded(state):
                print("object found")
                actions.insert(0, "take")
            
            print("get_actions: no danger zone found")
            global current_direction
            direction = current_direction
            while not is_valid_direction(direction, state):
                direction = get_direction(state)
            actions.insert(0, "goto" + str(direction + 1))
            
        else:
            print("get_actions: shreck founded (goto and joke)")
            print("directino = ", direction)
            actions.append("goto" + str(direction + 1))
            joke_direction = lookup_shreck(direction, state)
            print("get_actions: joke_direction:", joke_direction)
            actions.append("joke" + str(joke_direction))
    return actions

if __name__ == "__main__":
    while True:
        state = get_game_state()
        if ('yourTurn' in state and state['yourTurn'] == False) or 'yourTurn' not in state:
            time.sleep(0.5)
            continue

        actions  = get_actions(state)
        response = put_game_actions(state['currentTurn'], actions)
        print_state2array(state)

        

