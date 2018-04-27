import random
import os
from os.path import join
import re
from datetime import datetime, timedelta
from shutil import rmtree, copyfile
import pickle
import math
from PIL import Image


def get_name_by_list(names, separate='_'):
    name = ''
    for n in names:
        name += (n + separate)
    return name[:-1]


def generate_data(peoples_num=30, wifi_err_rate=0.1, video_err_rate=0.0, add_other_people=0):
    data_dir = 'PIE'
    all_peoples = os.listdir(data_dir)
    min_pic = 5
    max_pic = 20
    start_time = '10-22-12-00-00'
    meeting2_num = 10
    meeting3_num = 10
    meeting4_num = 5
    meeting5_num = 5
    meeting6_num = 5
    meeting7_num = 5
    meeting8_num = 5
    meeting9_num = 5
    meeting10_num = 5
    meeting20_num = 5


    random.seed(10)

    selected_people = random.sample(all_peoples, peoples_num)
    add_people = [p for p in all_peoples if p not in selected_people]
    add_people = random.sample(add_people, add_other_people)

    all_meeting = [2]*meeting2_num + [3]*meeting3_num + [4]*meeting4_num + [5]*meeting5_num + \
                  [6]*meeting6_num + [7]*meeting7_num + [8]*meeting8_num + [9]*meeting9_num + \
                  [10]*meeting10_num + [20]*meeting20_num

    start_time = datetime.strptime(start_time, '%m-%d-%H-%M-%S')
    true_label = {}
    data_folder_name = '%d_%1.1f_%1.1f_%d' % (peoples_num, wifi_err_rate, video_err_rate, add_other_people)
    print('\n_%s'%data_folder_name)
    if os.path.exists(data_folder_name):
        rmtree(data_folder_name)
    os.mkdir(data_folder_name)
    iou_id = 0

    for meeting_people_nun in all_meeting:
        end_time = start_time + timedelta(minutes=180)
        folder_name = '%s_%s'%(start_time.strftime('%m-%d-%H-%M-%S'), end_time.strftime('%m-%d-%H-%M-%S'))
        os.mkdir(join(data_folder_name, folder_name))
        os.mkdir(join(data_folder_name, folder_name, 'mtcnn'))
        meeting_people = random.sample(selected_people, meeting_people_nun)
        other_people = [p for p in selected_people if p not in meeting_people]
        if len(other_people) >= len(meeting_people):
            other_people = random.sample(other_people, meeting_people_nun)
        else:
            video_err_rate = video_err_rate * meeting_people_nun / len(other_people)

        sub_meeting_name = '%s_%s'%((start_time+timedelta(minutes=20)).strftime('%m-%d-%H-%M-%S'),
                                    (start_time+timedelta(minutes=40)).strftime('%m-%d-%H-%M-%S'))
        output_people = []
        for peo in meeting_people:
            pic_dirs = os.listdir(join(data_dir, peo))
            pic_num = random.randint(min_pic, max_pic)
            pic_dirs = random.sample(pic_dirs, pic_num)
            if random.random() > wifi_err_rate:
                output_people.append(peo)
            for pic in pic_dirs:
                img = Image.open(join(data_dir, peo, pic))
                img = img.resize((160, 160), Image.ANTIALIAS)
                img.save(join(data_folder_name, folder_name, 'mtcnn', '%s_%d_1.jpeg'%(sub_meeting_name, iou_id)))
                true_label['%s_%d_1.jpeg'%(sub_meeting_name, iou_id)] = peo
                iou_id += 1
        print('%s: %s'%(folder_name, get_name_by_list(meeting_people)))
        for peo in other_people:
            if random.random() < video_err_rate:
                output_people.append(peo)
        file = open(join(data_folder_name, folder_name, '-55_%s.png' % get_name_by_list(output_people)), 'w')
        file.close()
        print('output %s: %s' % (folder_name, get_name_by_list(output_people)))
        tmp_add = []
        for p in add_people:
            if random.random() < 0.05:
                pic_dirs = os.listdir(join(data_dir, p))
                pic_num = random.randint(min_pic, max_pic)
                pic_dirs = random.sample(pic_dirs, pic_num)
                tmp_add.append(p)
                for pic in pic_dirs:
                    img = Image.open(join(data_dir, p, pic))
                    img = img.resize((160, 160), Image.ANTIALIAS)
                    img.save(join(data_folder_name, folder_name, 'mtcnn', '%s_%d_1.jpeg' % (sub_meeting_name, iou_id)))
                    true_label['%s_%d_1.jpeg' % (sub_meeting_name, iou_id)] = 'other'
                    iou_id += 1
        print('video_add %s: %s' % (folder_name, get_name_by_list(tmp_add)))
        start_time = end_time

    with open(join(data_folder_name, 'true_label.pk'), 'wb') as f:
        pickle.dump(true_label, f, protocol=pickle.HIGHEST_PROTOCOL)


generate_data(30, 0.0, 0.0, 0)

for i in range(1, 6):
    generate_data(30, i / 10, 0, 0)
    generate_data(30, 0, i / 10, 0)
    generate_data(30, i / 10, i / 10, 0)

for i in range(2, 12, 2):
    generate_data(30, 0, 0, i)
