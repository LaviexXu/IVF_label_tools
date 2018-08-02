import json
import numpy

label_mapping = {
    'exception': 0,
    'tStart': 1,
    'tPNf': 2,
    't2': 3,
    't3': 4,
    't4': 5,
    't4+': 6,
}
with open('tmp.json') as json_file:
    video_infos = json.load(json_file)

fix_dimension_labels = {}
for video in video_infos:
    cur_video_info = video_infos[video]
    sorted_label = sorted(cur_video_info.items(), key=lambda k: int(k[0]))
    labels = list()
    break_flag = False
    for i in range(len(sorted_label)):
        if i < len(sorted_label)-1 and int(sorted_label[i+1][0]) < 300:
            length = int(sorted_label[i+1][0])-int(sorted_label[i][0])
        else:
            length = 300 - int(sorted_label[i][0])
            break_flag = True
        temp = [label_mapping[sorted_label[i][1]]]*length
        labels += temp
        if break_flag:
            fix_dimension_labels[video] = labels
            break

with open('fix_dimension_labels.json', "w") as f:
    json.dump(fix_dimension_labels, f)
