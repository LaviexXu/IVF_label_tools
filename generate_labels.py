import utils
import os
import numpy
import json
label_mapping = {
        'exception': 0,
        'tStart': 1,
        'tPNf': 2,
        't2': 3,
        't3': 4,
        't4': 5,
        't4+': 6,
    }


def labeling_single_video(video_info, last_frame_index):
    sorted_label = sorted(video_info.items(), key=lambda k: int(k[0]))
    labels = list()
    break_flag = False
    for i in range(len(sorted_label)):
        if i < len(sorted_label) - 1 and int(sorted_label[i + 1][0]) < last_frame_index:
            length = int(sorted_label[i + 1][0]) - int(sorted_label[i][0])
        else:
            length = last_frame_index - int(sorted_label[i][0])
            break_flag = True
        temp = [label_mapping[sorted_label[i][1]]]*length
        labels += temp
        if break_flag:
            return labels


def generate_json_labels(video_infos, last_frame_index):
    # video_infos should be loaded from json file.
    # last_frame_index refers to the length of useful frames
    fix_dimension_labels = {}
    for video in video_infos:
        cur_video_info = video_infos[video]
        label = labeling_single_video(cur_video_info, last_frame_index)
        fix_dimension_labels[video] = label
    return fix_dimension_labels


def generate_frames_and_labels_npz(video_infos, video_root, last_frame_index):
    for video in video_infos:
        video_path = os.path.join(video_root, video)
        frames = utils.read_video_frames(video_path)[:last_frame_index]
        cur_video_info = video_infos[video]
        labels = labeling_single_video(cur_video_info, last_frame_index)
        file_name = video.split('avi')[0]+'npz'
        file_folder = 'add the path you want to store the npz files'
        file_path = os.path.join(file_folder, file_name)
        numpy.savez(file_path, frames=frames, labels=labels)


if __name__ == '__main__':
    json_file_path = 'add the path of json file'
    videos_path = 'add the path where you store the videos'
    maximum_frame_index = 350
    with open(json_file_path) as json_file:
        video_infos = json.load(json_file)
    generate_frames_and_labels_npz(video_infos, videos_path, maximum_frame_index)
