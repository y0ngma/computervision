## 배경
- 기존에는 처리할 파일이 많을 경우 컴퓨터 여러대에서 일일이 나스를 접속하여 파일을 로컬로 받음
- 받은 파일을 로컬에서 코드 실행하여 일괄 처리
- 일괄 처리 중 용량이 하드용량이 가득차서 나스에 업로드함으로 하드 비울때까지 작업 지체 
- 컴퓨터가 3대 넘어가니 어떤 파일을 어디까지 처리했고 업로드(업체전달)했는지를 기록하는 엑셀 작성해야 했음
- 그 와중에 컴퓨터 마다 각기 저장용량 차이 때문에 외장하드도 사용
- 처리된 파일을 압축후 삭제 자동화를 하더라도 근본적으로 나스 다운로드/업로드 자동화가 필요했음
- 따라서 사내 여러 컴퓨터 자원을 편리하게 활용하기 위해 vagrant package으로 환경셋팅 배포
- 코드 및 vagrantfile은 깃 활용

## 프로세스
vagrant를 통한 우분투 가상환경내에서 NAS폴더에 접속하여 처리할 소스파일을 처리후 산출물을 다시 NAS에 업로드
1. vagrant 구동시 나스 폴더를 가상환경에 마운트
1. 처리 코드를 가상환경내에서 실행하여 마운트된 폴더내 파일을 처리
1. 산출물을 업로드
1. 업로드 후 삭제

## 추가 보완사항
- vagrantfile에 네트워크 설정으로 한대의 개발pc에서 여러 작업용pc로 접속 허용
- git, vagrant shared folder 등 활용

## 개발환경 셋팅
1. vagrant 설치
https://www.44bits.io/ko/post/vagrant-tutorial#%EA%B0%9C%EB%B0%9C-%ED%99%98%EA%B2%BD-%EA%B5%AC%EC%B6%95%EC%9D%84-%EC%9C%84%ED%95%9C-%ED%94%84%EB%A1%9C%EB%B9%84%EC%A0%80%EB%84%88

2. vagrantfile 작성을 위해 필요한 하드웨어/소프트웨어 사양 파악
    ```
    ## 서버 등에 접속하여 설치된 우분투 사양 파악
    # 리눅스 배포판 확인
    cat /etc/*release
    
    # 커널 버전 확인
    cat /proc/version
    uname -r
    
    # cpu 전체 정보
    cat /proc/cpuinfo
    
    # 메모리 정보
    free -h
    
    # 하드디스크 정보
    df -h
    
    # 그래픽카드 정보
    lspci | grep -i VGA
    
    # 엔비디아 경우에 다음 사용가능
    nvidia-smi
    ```
3. vagrantfile 작성
4. 
## 접속정보
```py
host    : 
guest   : 10.0.2.15

Forwarding ports...
    default: 80 (guest) => 8080 (host) (adapter 1)
    default: 22 (guest) => 2222 (host) (adapter 1)

ssh address     : 127.0.0.1:2222
ssh username    : vagrant
ssh auth method : private key
```
## Vagrant 명령어
- 박스
    - vagrant box add <address> : 박스 추가
    - vagrant box list          : 설치된 박스 리스트
    - vagrant box outdated      : 최신 업데이트 된 박스들 보여주기
    - vagrant box remove <address>  : 박스 삭제
        - 예:vagrant box remove ubuntu/bionic64 --box-version "20210609.0.0"
    - vagrant package           : 현재 실행중인 Virtualbox 를 재사용 가능한 box로 만든다.

- 상태
    - vagrant ssh               : ssh 접속
    - vagrant global-status     : 실행중 Vagrant environments. vagrant halt 등으로 꺼줘야 한다.
    - vagrant halt              : vagrant 끄기. 램에서도 삭제
    - vagrant suspend           : 저장 및 종료. vagrant up 하면 10초안에 재시작. 디스크와 램을 사용하는 상태로 종료
    - vagrant destroy           : 디스크에서 삭제. vagrant up 하면 다시 설치함.

- vagrant plugin
    - vagrant plugin install
    - vagrant plugin license
    - vagrant plugin list
    - vagrant plugin uninstall
    - vagrant plugin update

## 도커 명령어
```bash
# 우분투설치 및 우분투접속 후에 도커설치
curl -s https://get.docker.com | sudo sh

# 설치된 버전 확인
docker -v

# 추가된것확인
cat /etc/apt/sources.list.d/docker.list # deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable
dpkg --get-selections | grep docker 
# docker-ce     (엔진 : 서버에서 명령수행) 설치됨
# docker-ce-cli (클라 : 도커명령 서버에전달) 설치됨

```

## vagrant ssh 후 나스연결

### 시작할때 자동으로 마운트 시켜주기 위해선 fstab파일을 수정해야한다
- vagrant shared folder에 아래 키파일과 다운폴더를 위치시켜서 용이하게 이용한다
1. sudo mkdir -p /home/nas
    - '마운트시킬 NAS 경로'와 '로컬에서 해당 경로의 파일을 확인할수 있는 destination 경로'를 생성한다
1. sudo vim /home/.naspassword
    - 비밀번호 파일생성(파일명무관) 및 접속할 계정정보 입력
    ```bash
    username=사용자이름
    password=비밀번호
    ```
1. sudo vim /etc/fstab
    - 위에서 확인한 경로 3가지를 다음과 같이 입력한다
    - [//ip주소/나머지src경로] [로컬dst경로] cifs credentials=[/비번파일경로] 
    ```bash
    //192.168.0.12/homes/ /home/nas cifs credentials=/home/.naspassword,rw 0 0
    ```
1. sudo mount --all
    - 저장 후 곧바로 실행시키기


## 파이선 및 라이브러리 설치
## 파이선 코드 실행
- l
```bash
python3.8 /vagrant/SHARED_FOLDER/test.py
```

### 에러로그
```bash
## 마운트할 폴더 경로 한번에 생성
vagrant@ubuntu-bionic:/home$ sudo mkdir -p qtumai/jason/nas/
vagrant@ubuntu-bionic:/home$ cd qtumai/jason/

## 잘못된 문법
vagrant@ubuntu-bionic:/home/qtumai/jason$ sudo mount -t cifs 192.168.0.12:/homes ./nas
mount.cifs: bad UNC (192.168.0.12:/homes)

## 터미널에서 who am i 으로 사용자 확인시 vagrant이기 때문에 안되나?
vagrant@ubuntu-bionic:/home/qtumai/jason$ sudo mount -t cifs //192.168.0.12/homes ./nas
Password for root@//192.168.0.12/homes:  **********
mount error(13): Permission denied
Refer to the mount.cifs(8) manual page (e.g. man mount.cifs)

## 사용자계정을 지정하니 접속됨
vagrant@ubuntu-bionic:/home/qtumai/jason$ sudo mount -t cifs //192.168.0.12/homes ./nas -o username=사용자계정명
Password for admin@//192.168.0.12/homes:  **********

## 드라이브 마운트 확인
vagrant@ubuntu-bionic:/home/qtumai/jason$ df -h
Filesystem            Size  Used Avail Use% Mounted on
...
//192.168.0.12/homes   11T  7.7T  2.9T  73% /home/qtumai/jason/nas
# 다만, 위의 방법으로는 한번만 마운트되어 접속시마다 해줘야함

## 마운트된 나스파일을 베이그란트 shared_folder로 복사에러
PermissionError: [Errno 13] Permission denied:
# 원인은 쓰기권한이 없어서 였음 [유저]:[유저그룹] [경로]
sudo chown -R vagrant:vagrant jason # 일단 소유권 변경으로 chmod 수정권한 획득
sudo chmod -R 777 jason # r-x를 rwx로 해당 쓰기권한 부여
# https://codechacha.com/ko/linux-chmod/
```