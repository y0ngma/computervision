import datetime, time
import os, glob, zipfile
import pickle
import pandas as pd



def zip_with_filecount_suffix( _src_path, dest_file ):
    cnt = 0
    print( '압축대상 {}\n압축이름 {}\n압축중...'.format(_src_path,dest_file) )
    with zipfile.ZipFile( dest_file, 'w', zipfile.ZIP_DEFLATED ) as zf:
        _rootpath = _src_path
        for ( _dirpath, dirnames, filenames ) in os.walk( _src_path ):
            for filename in filenames:
                _target_path = os.path.join( _dirpath, filename )
                cnt += 1
                _rel_path = os.path.relpath( _target_path, _rootpath )
                zf.write( _target_path, _rel_path )
    print('압축 완료 !')
    new_file_path = dest_file.split('.')[0]+'_{}EA.zip'.format(cnt)
    try:
        os.rename( dest_file, new_file_path )
    except FileExistsError as e:
        print('이름바꾸기 실패하여 pass함 ',e)
        pass
    


def update_log_df(log_file, log_list_of_list):
    '''
    변환한 동영상 폴더별 파일갯수 파악하여 기존엑셀에 추가
    log_file         : 로그 엑셀파일과 그 풀경로
    log_list_of_list : 변환된 이미지폴더명과 그 안의 파일 갯수 등으로 이루어진 [[date,.., folder, count], [],[],..]
    '''
    if not os.path.exists(log_file): # 최초실행시 작동
        df_old = pd.DataFrame()
        print('로그파일이 존재하지 않음', log_file)
        df_old.to_excel(log_file)
    df_old = pd.read_excel(log_file, index_col=0)
    df_to_append = pd.DataFrame(log_list_of_list, columns=['converted_date','converted_time','basename','folder_name','file_count'])
    print(df_to_append)
    df_new = pd.concat([df_old,df_to_append])
    df_new.to_excel(log_file)



def aimmo_xlsx(log_file, target_path:str):
    """
    aimmo제출용 "idx", "체널2", "체널1", "체널2파일수", "체널1파일수"를 컬럼으로 갖는 엑셀만들기 
    """
    def idx_from_1(df:pd.DataFrame):
        # df의 인덱스가 1부터 시작하게끔 하는 방법 2가지
        if df.index[0]==0:
            df.index = df.index + 1
        else:
            import numpy as np
            df.index = np.arange(1,len(df)+1)

    # 한 폴더내에 채널별로 저장된 폴더명(*_ch1, *_ch2)과 해당 폴더내 파일수 측정
    folder_ch1 = [ os.path.basename(path) for path in sorted(glob.glob(target_path+"/*ch1")) ]
    folder_ch2 = [ os.path.basename(path) for path in sorted(glob.glob(target_path+"/*ch2")) ]
    ch1_cnt    = [ len(os.listdir(path))  for path in sorted(glob.glob(target_path+"/*ch1")) ]
    ch2_cnt    = [ len(os.listdir(path))  for path in sorted(glob.glob(target_path+"/*ch1")) ]
    both_channel = list(zip(folder_ch2, folder_ch1, ch2_cnt, ch1_cnt))
    # print(*both_channel, sep='\n')
    cols = ['left', 'right', 'ch2_cnt', 'ch1_cnt']
    to_append  = pd.DataFrame(both_channel, columns=cols)
    bookmarker = pd.DataFrame([["+"*20, "+"*20, "+"*5, "+"*5]], columns=cols)
    idx_from_1(to_append)
    print(to_append)
    # 기존 로그 엑셀파일 읽어들여서 업데이트 하기        
    if not os.path.exists(log_file):
        df_old = pd.DataFrame()
        df_old.to_excel(log_file)
    df_old = pd.read_excel(log_file, index_col=0, engine='openpyxl')
    df_old = pd.concat([df_old, to_append])
    df_old = pd.concat([df_old, bookmarker])
    df_old.to_excel(log_file)
        


if __name__ == "__main__":
    PROJECT_DIR      = os.path.dirname( os.path.abspath(__file__) )
    base_path        = "C:/Users/home/qtumai/jason/SYNCED_FOLDER"
    target_path_list = glob.glob(base_path+'/*_image')
    
    for target_path in target_path_list:
        aimmo_xlsx(PROJECT_DIR+"/log_aimmo.xlsx", target_path)
