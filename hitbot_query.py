#! /usr/bin/python3

import json
import urllib.request

def GetFrameData(fighter_name, move_search):
    fighter_name = fighter_name.title().replace(" ", "%20")
    move_search = move_search.title()
    # Check if HitboxActive is null (for moves like throws)
    try:
        url = urllib.request.urlopen(
            'https://api.kuroganehammer.com/api/characters/name/'
            + fighter_name + '/moves?game=ultimate&expand=true')
        json_data = url.read()

        frame_data = []

        fighter = json.loads(json_data)
        for move in fighter:
            move_data = []
            index = fighter.index(move)
            if fighter[index]['Name'].find(move_search) != -1:
                move_data.append(fighter[index]['Name'])
                move_data.append(fighter[index]['HitboxActive']['Frames'])
                move_data.append(fighter[index]['HitboxActive']['Adv'])
                move_data.append(fighter[index]['BaseDamage']['OneVOne'])
                move_data.append(fighter[index]['FirstActionableFrame'])
                move_data.append(fighter[index]['Angle'])
                move_data.append(fighter[index]['BaseKnockBackSetKnockback'])
                move_data.append(fighter[index]['KnockbackGrowth'])
                frame_data.append(move_data)

    except urllib.error.URLError as url_error:
        if url_error.code == 404:
            frame_data = 'Character not found'
        else:
            print("URL Error code:", url_error.code)
            frame_data = 'Error fetching data'

    return frame_data
