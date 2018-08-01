import cv2
import os
import time
start_time = time.time()
import json
from utils import *
import numpy as np


def logging(info):
    print('[{:.2} min] {}'.format((time.time() - start_time)/60, info))


# data_root = Add your folder path of videos here
data_root = 'J:/AI_Video'

tmp = 'tmp.json'
winname = '[{}], project_index: [{}/{}], pic_progress: [{}/{}]'
keyvalue = {
    '2': 50,
    '3': 51,
    '4': 52,
    '5': 53,
    'a': 97,
    'd': 100,
    'i': 105,
    'q': 113,
    't': 116,
    'e': 101,
    'y': 121,
    'z': 122,
    '[': 91,
    ']': 93,
    'l': 108,
    'esc': 27

}


if os.path.exists(tmp):
    with open(tmp) as jsonf:
        infos = json.load(jsonf)
else:
    infos = {}


errors = []
videos = os.listdir(data_root)
logging('Total number from data_root: {}'.format(len(videos)))
length = len(videos)
keys_init = list(infos.keys())
pro_idx_init = np.array([True if item in keys_init else False for item in videos])
project_index = np.min(np.where(pro_idx_init == False)[0])

jumped = False

# for i in range(start, len(folds)):
while (1):
    project_index = np.max([0, project_index])
    project_index = np.min([project_index, len(videos) - 1]) # clip project index

    video = videos[project_index]
    video_path = os.path.join(data_root, video)
    frames = read_video_frames(video_path)
    index = 0
    try:
        video_infos = infos[video]
    except KeyError:
        infos[video] = {}

    # cv2.namedWindow(winname.format(fold, project_index, length))
    cv2.namedWindow('label image software')
    last_key = ''
    while True:
        jupmed = False
        index = np.max([0, index])
        index = np.min([index, len(frames) - 1])
        img = frames[index]
        # windwwow = cv2.namedWindow(winname.format(fold, project_index, length))
        cv2.imshow('label image software', img)
        print(winname.format(video, project_index, length, index, len(frames)))
        if video in infos.keys() and infos[video] != {}:
            print(infos[video])
        c = cv2.waitKey()
        if c == keyvalue['esc']:
            exit()
        elif c == keyvalue['q']:
            index -= 1
        elif c == keyvalue['e']:
            index += 1
        elif c == keyvalue['a']:
            index -= 12
        elif c == keyvalue['d']:
            index += 12
        elif c == keyvalue['l']:
            infos[video][str(index)] = 'exception'
            last_key = str(index)
            with open(tmp, "w") as f:
                json.dump(infos, f)
                logging('write {} in {}'.format('exception', video))
        elif c== keyvalue['i']:
            infos[video][str(index)] = 'tStart'
            last_key = str(index)
            with open(tmp, "w") as f:
                json.dump(infos, f)
                logging('save {} in {} succeed'.format('tStart time', video))

        elif c == keyvalue['t']:
            infos[video][str(index)] = 'tPNf'
            last_key = str(index)
            with open(tmp, "w") as f:
                json.dump(infos, f)
                logging('save {} in {} succeed'.format('tPNf time', video))

        elif c == keyvalue['2']:
            infos[video][str(index)] = 't2'
            last_key = str(index)
            with open(tmp, "w") as f:
                json.dump(infos, f)
                logging('save {} in {} succeed'.format('t2 time', video))

        elif c == keyvalue['3']:
            infos[video][str(index)] = 't3'
            with open(tmp, "w") as f:
                json.dump(infos, f)
                logging('save {} in {} succeed'.format('t3 time', video))

        elif c == keyvalue['4']:
            infos[video]['t4'] = int(index)
            last_key = str(index)
            with open(tmp, "w") as f:
                json.dump(infos, f)
                logging('save {} in {} succeed'.format('t4 time', video))

        elif c == keyvalue['5']:
            infos[video][str(index)] = 't4+'
            last_key = str(index)
            with open(tmp, "w") as f:
                json.dump(infos, f)
                logging('save {} in {} succeed'.format('t4+ time', video))
        elif c == keyvalue['z']:
            if last_key != '':
                try:
                    del infos[video][last_key]
                except KeyError:
                    pass
        elif c == keyvalue['[']:
            project_index -= 1
            if infos[video] == {}:
                del infos[video]
            break
        elif c == keyvalue[']']:
            project_index += 1
            if infos[video] == {}:
                del infos[video]
            break
        else:
            pass
