import json
import datetime


def makeJSON(temp, humid, motion, light):
    data = {}
    data['temp'] = temp
    data['humid'] = humid
    #data['head_count'] = 4
    data['video_state'] = motion
    data['light_condition'] = light
    data['audio_state'] = "silent"
    data['time'] = str(datetime.datetime.now())

    json_data = json.dumps(data)

    print(json_data)

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

