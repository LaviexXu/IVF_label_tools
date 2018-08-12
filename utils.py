from datetime import datetime
import time
import cv2


def filter_pic(pics):
    pics = [
        item for item in pics if item[:2] != 'EM' and item[-3:] == 'jpg'
    ]
    pics = [
        (item, time_resolve(item)) for item in pics
    ]
    pics = sorted(pics, key=lambda x: x[1])
    pics = [item[0] for item in pics]
    return pics


def time_resolve(name):
    name = name[name.index('_') + 1: name.index('.')]
    rtime = time.strptime(name, '%Y_%m_%d_%H_%M')
    return rtime


def name_resolve(name):
    return name[name.index('_') + 1: name.index('.')]


def read_video_frames(path):
    video = cv2.VideoCapture(path)
    frames = list()
    if video.isOpened():
        rval, cur_frame = video.read()
        frames.append(cur_frame)
        while rval:
            rval, cur_frame = video.read()
            frames.append(cur_frame)
    video.release()
    return frames


def read_video_frames(path, size):
    video = cv2.VideoCapture(path)
    frames = list()
    if video.isOpened():
        rval, cur_frame = video.read()
        frames.append(cur_frame)
        while rval:
            rval, cur_frame = video.read()
            cur_frame = cv2.resize(cur_frame, (size, size), interpolation=cv2.INTER_LINEAR)
            frames.append(cur_frame)
    video.release()
    return frames


def resize_frames(frames, size):
    resized_frames = list()
    for frame in frames:
        r_frame = cv2.resize(frame, (size, size), interpolation=cv2.INTER_LINEAR)
        resized_frames.append(r_frame)
    return resized_frames
