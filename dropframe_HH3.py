import cv2
import os, glob, shutil, zipfile
import datetime, time
import pandas as pd, re
from myfunctions import zip_with_filecount_suffix, update_log_df, aimmo_xlsx


PROJECT_DIR    = os.path.dirname(os.path.abspath(__file__))+"\\"
# DOWNLOAD_DIR = "C:/Users/home/qtumai/jason/SYNCED_FOLDER"
DOWNLOAD_DIR = "/home/qtumai/jason/SYNCED_FOLDER"
archive_path = "/home/qtumai/jason/SYNCED_FOLDER"
print('작업파일의 경로:', PROJECT_DIR)

original_fps   = 30 # 변환할 원본영상의 fps
fps_list       = 30 # 영상에서 가져올 프레임 간격
log_path       = archive_path # 로그보관용 폴더경로
hour_list      = [ '00','01','02','03','04','05','06','07','08','09','10','11',
                   '12','13','14','15','16','17','18','19','20','21','22','23' ]
                   
# 압축해제 폴더의 동영상 파일 읽어서 변환활 폴더 생성
unplayable_video = list()
worked_dirs      = list()
for file in glob.glob( DOWNLOAD_DIR+'*.avi' ):
    FILE_TO_WORK     = True
    video_name       = os.path.splitext(file)[0].split('\\')[-1]
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
        original_path = archive_path + basename +'_ori\\'
        if not os.path.isdir(original_path):
            os.makedirs(original_path, exist_ok=True)
            print('생성된 경로', original_path)

        # 1000번째까지의 작업한 사진 저장경로(업체요청)
        worked_dirs.append(archive_path + basename +"_image\\")
        save_path = archive_path + basename +"_image\\"+ new_video_name +'\\'
        if not os.path.isdir(save_path):
            os.makedirs(save_path, exist_ok=True)
            print('생성된 경로', save_path)

        # 파일명에서 120000~235959에 해당하는것만 변환
        target_hours = hour_list[12:24]
        if video_shopname == "DONJJANG": # 특성상 오전포함, 야간제외
            target_hours = hour_list[8:20]

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
                shutil.move( file, os.path.join(original_path, file.split('\\')[-1]) )
                print( '여기서 {} -->\n여기로 {}'.format(file, os.path.join(original_path, file.split('\\')[-1])) )
                

print( "문제가 생긴 영상 : ", *unplayable_video, sep='\n' )
for worked_dir in worked_dirs:
    if os.path.isdir(worked_dir):
        aimmo_xlsx(log_path+"log_aimmo.xlsx", worked_dir) # 에이모제공용 엑셀 업데이트
        zip_with_filecount_suffix(worked_dir, worked_dir+'.zip') # 압축하기



