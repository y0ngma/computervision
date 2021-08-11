#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, os, sys, shutil
import time, datetime
# import numpy as np
import pandas as pd
import cv2
from myfunctions import zip_with_filecount_suffix, update_log_df, aimmo_xlsx


# NAS_DIR = "//192.168.0.12/homes/brooks/DONJJANG"
# NAS_DIR = "/home/qtumai/jason/nas/dataset" # vagrant destory 후 ~homes으로 변경되면
NAS_DIR = "/home/qtumai/jason/nas"
# DOWNLOAD_DIR = 'C:/Users/home/qtumai/jason/SYNCED_FOLDER'
DOWNLOAD_DIR = '/home/qtumai/jason/SYNCED_FOLDER' # 싱크폴더로 저장하면 호스트에서 접근하기 용이
archive_path = "/home/qtumai/jason/SYNCED_FOLDER"

target_shop = 'DONJJANG'
target_dates = [
# "20210804",
# "20210805",
"20210806",
"20210807",
"20210808",
]
hour_list      = [ '00','01','02','03','04','05','06','07','08','09','10','11',
                   '12','13','14','15','16','17','18','19','20','21','22','23' ]
target_hours   = hour_list[12:23]



# all_file_list    = [ file for file in glob.glob(NAS_DIR +"/*.avi") if os.path.getsize(file)>920000000 ]
# print('조회된 파일 수 :', len(all_file_list))
# target_path_list = list()
# file_size_list   = list()
# duration_list    = list()
# # 전체 파일리스트에서 파일명의 날짜와 상호명으로 원하는것만 작업
# for file_path in all_file_list:
#     filename         = os.path.basename(file_path)
#     video_name       = os.path.splitext( filename )[0]
#     video_datetime   = video_name.split('_')[0]
#     video_shopname   = video_name.split('_')[1]
#     if video_shopname != target_shop: continue
#     else:
#         video_date = video_datetime[:8]
#         video_hour = video_datetime[8:10]
#         for target_date in target_dates:
#             if video_date != target_date: continue
#             else:
#                 # 업소별 특징 적용 1. 어두운 거리 특성상 오전포함, 야간제외
#                 if video_shopname == "DONJJANG":
#                     target_hours = hour_list[8:20]
#                 video_camnumber  = video_name.split('_')[2]
#                 # 업소별 특징 적용 2.업체 요청으로 좌우 채널명 교환
#                 if video_shopname == "SW365":
#                     if video_name.split('_')[2] == "ch1":
#                         video_camnumber = "ch2"
#                     if video_name.split('_')[2] == "ch2":
#                         video_camnumber = "ch1"
                
#                 for target_hour in target_hours:
#                     if video_hour == target_hour:
#                         # 비디오 길이측정
#                         print('영상길이측정중... : ', file_path)
#                         cap = cv2.VideoCapture(file_path)
#                         cnt = cap.get(cv2.CAP_PROP_FRAME_COUNT)
#                         fps = cap.get(cv2.CAP_PROP_FPS)
#                         cap.release()
#                         if fps == 0: continue
#                         else:
#                             seconds  = int(cnt/fps)
#                             duration = datetime.timedelta(seconds=seconds)
#                             min      = int( str(duration).split(":")[-2] )
#                             # 목표파일, 파일용량, 비디오길이 리스트 생성
#                             duration_list.append(min)
#                             target_path_list.append(file_path)
#                             file_size_list.append( os.path.getsize(file_path) )

# zipped_lists = list( zip(target_path_list, file_size_list, duration_list,) )
# df = pd.DataFrame( zipped_lists, columns=['path', 'size', 'duration'] )
# print(df.head())
# print(df.groupby(by=['duration']).count())

# workable_list = df[df['duration']>=24]['path'].to_list()
# print( '사용가능 파일 갯수= {}, 비율= {}%'.format(
#     len(workable_list), int(100*len(workable_list)/len(target_path_list))) )



# # 파일을 로컬로 이동
# for workable in workable_list:
#     filename = os.path.basename(workable)
#     print('나스->로컬경로 :', DOWNLOAD_DIR +"/"+ filename, 'copyfile 하는중...')
#     shutil.copyfile(workable, DOWNLOAD_DIR +"/"+ filename)
# print('이동완료')


#####################################################################################
# 변환 작업
original_fps     = 30 # 변환할 원본영상의 fps
fps_list         = 30 # 영상에서 가져올 프레임 간격
log_path         = archive_path # 로그보관용 폴더경로
unplayable_video = list()
worked_dirs      = list()
for file in glob.glob( DOWNLOAD_DIR+'/*.avi' ):
    FILE_TO_WORK     = True
    video_name       = os.path.splitext(file)[0].split('/')[-1]
    if video_name[:4] == '2021' and video_name[14] == '_':
        video_datetime   = video_name.split('_')[0]
        video_shopname   = video_name.split('_')[1]
        video_camnumber  = video_name.split('_')[2]
        if video_shopname == "SW365": # 업체 요청으로 좌우 채널명 교환
            if video_name.split('_')[2] == "ch1":
                video_camnumber = "ch2"
            if video_name.split('_')[2] == "ch2":
                video_camnumber = "ch1"
        video_date       = video_datetime[:8]
        video_hour       = video_datetime[8:10]
        video_minute     = video_datetime[10:12]
        video_second     = video_datetime[12:video_name.find('_')]
        str_HHMMSS       = video_hour +":"+ video_minute +":"+ video_second
        str_HHMMSS       = datetime.datetime.strptime(str_HHMMSS, "%H:%M:%S")
        video_time       = video_hour + video_minute + video_second
        date_time_prefix = video_date+'_'+video_time

        # "년월일_시분초_매장코드_캠번호" 따위로 파일명 수정 및 저장폴더명 설정
        new_video_name   = date_time_prefix +"_"+ video_shopname +"_"+ video_camnumber # 19991231_235959_JJIN_ch2
        basename         = video_shopname +'_'+ video_date # JJIN_19991231

        # 작업한 원본영상 옮겨놓을 경로 
        FPS           = '_' + str(1 + original_fps - fps_list) + 'FPS'
        original_path = archive_path +'/'+ basename +'_ori/'
        if not os.path.isdir(original_path):
            os.makedirs(original_path, exist_ok=True)
            print('생성된 경로', original_path)

        # 1000번째까지의 작업한 사진 저장경로(업체요청)
        worked_dirs.append(archive_path +"/"+ basename +"_image")
        save_path = archive_path +"/"+ basename +"_image/"+ new_video_name +'/'
        if not os.path.isdir(save_path):
            os.makedirs(save_path, exist_ok=True)
            print('생성된 경로', save_path)

        # 파일명에서 120000~235959에 해당하는것만 변환
        target_hours = hour_list[12:24]
        if video_shopname == "DONJJANG": # 특성상 오전포함, 야간제외
            target_hours = hour_list[7:20]

        for target_hour in target_hours:
            flag = False
            if video_hour == target_hour:
                # 영상의 프레임 정보를 가져와서 1초에 1프레임씩 저장
                video_cap  = cv2.VideoCapture(file, )
                cnt        = 0
                start_time = datetime.datetime.now()
                while True:
                    ret, image = video_cap.read()
                    if not ret:
                        if flag == False:
                            print( '안되는 영상', new_video_name)
                            unplayable_video.append( file )
                        break
                    flag       = True
                    fps        = int(video_cap.get(cv2.CAP_PROP_FPS))
                    frame      = int(video_cap.get(1))
                    if frame % fps_list == 0:
                        # frame1 -> frame0000001 으로 자리수 맞춰주기(업체요청)
                        try:
                            frame_str = str(frame)
                            if len(frame_str)   == 1:
                                frame_str = '00000000'+frame_str
                            elif len(frame_str) == 2:
                                frame_str = '0000000'+frame_str
                            elif len(frame_str) == 3:
                                frame_str = '000000'+frame_str
                            elif len(frame_str) == 4:
                                frame_str = '00000'+frame_str
                            elif len(frame_str) == 5:
                                frame_str = '0000'+frame_str
                            elif len(frame_str) == 6:
                                frame_str = '000'+frame_str
                            elif len(frame_str) == 7:
                                frame_str = '00'+frame_str
                            elif len(frame_str) == 8:
                                frame_str = '0'+frame_str
                            
                            # 녹화시점의 시간변수에 1초를 더한것을 파일명으로 저장(1초에 1장만 저장될때)
                            sec_to_add  = datetime.timedelta(seconds=1)
                            str_HHMMSS += sec_to_add
                            str_time    = datetime.datetime.strftime(str_HHMMSS, '%H%M%S')
                            time_infix  = video_date+'_'+str_time
                            save_name   = 'frame{}_{}_{}.jpg'.format(frame_str, time_infix, video_camnumber)

                            cv2.imwrite( save_path+save_name, image )
                            cnt += 1
                            
                            # 1000장까지만 작업하기(업체요청)
                            if cnt == 1000:
                                break

                        except Exception as e:
                            print(e)
                            # cv2.imshow('이미지 확인', image)
                            # cv2.waitKey()
                            continue

                        print( "Saved frame: "+str(frame)+", fps: "+str(fps),"파일명",save_name)
                        
                video_cap.release()
                end_time  = datetime.datetime.now()
                work_time = end_time - start_time
                print("Save %d images//work_time %s" % (cnt, work_time))
                
                # 작업이 끝난 원본파일을 따로 옮겨서 정리
                shutil.move( file, os.path.join(original_path, file.split('/')[-1]) )
                print( '여기서 {} -->\n여기로 {}'.format(file, os.path.join(original_path, file.split('/')[-1])) )
                

print( "문제가 생긴 영상 : ", *unplayable_video, sep='\n' )
for worked_dir in worked_dirs:
    if os.path.isdir(worked_dir):
        print(worked_dir)
        aimmo_xlsx(log_path+"/log_aimmo.xlsx", worked_dir) # 에이모제공용 엑셀 업데이트
        # zip_with_filecount_suffix(worked_dir, worked_dir+'.zip') # 압축하기

##########################################################################################################






# # 영상길이가 24분 이하일 경우 1000장보다 적게 이미지변환 될 수 있음
# df23 = df[df['duration']< 24]
# move_file_list = df[df['duration']<24]['path'].to_list()
# move_dst_path = NAS_DIR+"/small_file"
# if not os.path.isdir(NAS_DIR+"/small_file"):
#     os.mkdir(move_dst_path)
# print('경로생성')
# for move_file in move_file_list:
#     file_name = move_file.split("/")[-1]
#     shutil.move(move_file, move_dst_path+"/"+file_name)



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

