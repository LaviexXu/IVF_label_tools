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


def labeling_single_video(video_info, origin_frames, last_frame_index):
    sorted_label = sorted(video_info.items(), key=lambda k: int(k[0]))
    labels = list()
    frames = list()
    break_flag = False
    for i in range(len(sorted_label)):
        if i < len(sorted_label) - 1 and int(sorted_label[i + 1][0]) < last_frame_index:
            length = int(sorted_label[i + 1][0]) - int(sorted_label[i][0])
            if int(sorted_label[i][0]) == 0:
                last_frame_index += length
                continue
        else:
            if int(sorted_label[i][0]) == 0:
                raise IndexError
            length = last_frame_index - int(sorted_label[i][0])
            break_flag = True
        temp = [label_mapping[sorted_label[i][1]]] * length
        labels += temp
        frames += origin_frames[int(sorted_label[i][0]):int(sorted_label[i][0])+length]
        if break_flag:
            return labels, frames


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
        ori_frames = utils.read_video_frames(video_path)
        cur_video_info = video_infos[video]
        labels, frames = labeling_single_video(cur_video_info, ori_frames, last_frame_index)
        file_name = video.split('avi')[0]+'npz'
        file_folder = 'add the path you want to store the npz files'
        file_path = os.path.join(file_folder, file_name)
        numpy.savez(file_path, frames=frames, labels=labels)


def early_fusion_data(frames, context_frame_num):
    # there are totally 2*context_frame_num+1 context frames in one list
    fusion_data = list()
    for i in range(len(frames)):
        if i < context_frame_num:
            context_frames = [frames[0]]*(context_frame_num-i)
            context_frames += frames[:i+context_frame_num+1]
            fusion_data.append(context_frames)
        elif i >= len(frames)-context_frame_num:
            context_frames = frames[i-context_frame_num:]
            context_frames += [frames[-1]]*(context_frame_num+i-len(frames)+1)
            fusion_data.append(context_frames)
        else:
            fusion_data.append(frames[i-context_frame_num:i+context_frame_num+1])
    return fusion_data


