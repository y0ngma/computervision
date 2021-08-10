#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, os, sys, shutil
import time, datetime
# import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import cv2

# archive_path = "//192.168.0.12/homes/Jason/test_video"
# archive_path = "//192.168.0.12/homes/brooks/DONJJANG"
archive_path = "/home/qtumai/jason/nas"
archive_path = "D:/새 폴더"

MOVE_PATH = 'D:/'
# MOVE_PATH = 'C:/Users/home/qtumai/jason/computervision/SHARED_FOLDER'

target_shop = 'DONJJANG'
target_date = [
"20210804",
"20210805",
"20210806",
"20210807",
"20210808",
]

all_file_list = [ file for file in glob.glob(archive_path +"/*.avi") if os.path.getsize(file)>900000000 ]

target_path_list = list()
file_size_list   = list()
duration_list    = list()
# 전체 파일리스트에서 파일명의 날짜와 상호명으로 원하는것만 작업
for file_path in all_file_list:
    filename         = os.path.basename(file_path)
    video_name       = os.path.splitext( filename )[0]
    video_datetime   = video_name.split('_')[0]
    video_shopname   = video_name.split('_')[1]
    if video_shopname != target_shop: continue
    else:
        video_camnumber  = video_name.split('_')[2]
        if video_shopname == "SW365": # 업체 요청으로 좌우 채널명 교환
            if video_name.split('_')[2] == "ch1":
                video_camnumber = "ch2"
            if video_name.split('_')[2] == "ch2":
                video_camnumber = "ch1"
        video_date       = video_datetime[:8]
        for date in target_date:
            if video_date != date: continue
            else:
                video_hour       = video_datetime[8:10]
                video_minute     = video_datetime[10:12]
                video_second     = video_datetime[12:video_name.find('_')]
                str_HHMMSS       = video_hour +":"+ video_minute +":"+ video_second
                str_HHMMSS       = datetime.datetime.strptime(str_HHMMSS, "%H:%M:%S")
                video_time       = video_hour + video_minute + video_second
                date_time_prefix = video_date+'_'+video_time
                # 비디오 길이측정
                cap = cv2.VideoCapture(file_path)
                cnt = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                fps = cap.get(cv2.CAP_PROP_FPS)
                cap.release()
                if fps == 0: continue
                else:
                    seconds  = int(cnt/fps)
                    duration = datetime.timedelta(seconds=seconds)
                    min      = int( str(duration).split(":")[-2] )
                    # 목표파일, 파일용량, 비디오길이 리스트 생성
                    duration_list.append(min)
                    target_path_list.append(file_path)
                    file_size_list.append( os.path.getsize(file_path) )

zipped_lists = list( zip(target_path_list, file_size_list, duration_list,) )
df = pd.DataFrame( zipped_lists, columns=['path', 'size', 'duration'] )
print(df.head())
print(df.groupby(by=['duration']).count())

workable_list = df[df['duration']>=24]['path'].to_list()
print( '사용가능 파일 갯수= {}, 비율= {}%'.format(
    len(workable_list), int(100*len(workable_list)/len(target_path_list))) )

# for workable in workable_list:
#     filename         = os.path.basename(workable)
#     video_name       = os.path.splitext( filename )[0]
#     video_datetime   = video_name.split('_')[0]
#     video_shopname   = video_name.split('_')[1]
#     video_camnumber  = video_name.split('_')[2]
#     if video_shopname == "SW365": # 업체 요청으로 좌우 채널명 교환
#         if video_name.split('_')[2] == "ch1":
#             video_camnumber = "ch2"
#         if video_name.split('_')[2] == "ch2":
#             video_camnumber = "ch1"
#     video_date       = video_datetime[:8]
#     video_hour       = video_datetime[8:10]
#     video_minute     = video_datetime[10:12]
#     video_second     = video_datetime[12:video_name.find('_')]
#     str_HHMMSS       = video_hour +":"+ video_minute +":"+ video_second
#     str_HHMMSS       = datetime.datetime.strptime(str_HHMMSS, "%H:%M:%S")
#     video_time       = video_hour + video_minute + video_second
#     date_time_prefix = video_date+'_'+video_time
    
#     # 파일을 로컬로 이동
#     if video_shopname == target_shop:
#         for date in target_date:
#             if video_date == date:
#                 print(workable)
#                 print(MOVE_PATH +"\\"+ filename)
#                 # shutil.move(workable, MOVE_PATH +"\\"+ filename)
#     else:
#         # print('본파일의 {}는 원하는 상호명이 아니므로 넘어감'.format(video_shopname))
#         pass


# 변환 작업



# # 영상길이가 24분 이하일 경우 1000장보다 적게 이미지변환 될 수 있음
# df23 = df[df['duration']< 24]
# move_file_list = df[df['duration']<24]['path'].to_list()
# move_dst_path = archive_path+"\\small_file"
# if not os.path.isdir(archive_path+"\\small_file"):
#     os.mkdir(move_dst_path)
# print('경로생성')
# for move_file in move_file_list:
#     file_name = move_file.split("\\")[-1]
#     shutil.move(move_file, move_dst_path+"\\"+file_name)



# plt.hist(file_size_list, color='c', bins=10 )
# plt.xlabel('file_size')
# plt.ylabel('frequency')
# plt.title('histogram')
# plt.grid()
# plt.show()

# small_size = np.quantile(file_size_list, 0.9)
# df1 = df[ (df['size'] < df['size'].quantile(0.5)) & (df['size'] > df['size'].quantile(0.3)) ]
# df2 = df[ df['size']<df['size'].quantile(0.1) ]
# df3 = df[ df['size']>df['size'].quantile(0.99) ]

# for idx in range(df2.shape[0]):
#     file_path = df2.iloc[idx,0]
#     file_size = df2.iloc[idx,1]
#     cap = cv2.VideoCapture(file_path)
#     cnt = cap.get(cv2.CAP_PROP_FRAME_COUNT)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     seconds = int(cnt/fps)
#     duration = datetime.timedelta(seconds=seconds)
#     print( "경로{:<34}, 크기= {:_>10}, 길이= {}".format(file_path, file_size, duration) )
    
# mod = sys.modules[__name__]
# for idx in range(1,11):
#     setattr(mod, 'quantile0{}'.format(idx), idx)

# for idx in range(1,11):
#     globals()[ 'quantile0{}'.format(idx) ]=1

# print(quantile02)

