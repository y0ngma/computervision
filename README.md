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
    - vagrant remove <address>  : 박스 삭제
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

## 도커
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

### 에러로그
```bash
# 마운트할 폴더 경로 한번에 생성
vagrant@ubuntu-bionic:/home$ sudo mkdir -p qtumai/jason/nas/
vagrant@ubuntu-bionic:/home$ cd qtumai/jason/

# 잘못된 문법
vagrant@ubuntu-bionic:/home/qtumai/jason$ sudo mount -t cifs 192.168.0.12:/homes ./nas
mount.cifs: bad UNC (192.168.0.12:/homes)

# 터미널에서 who am i 으로 사용자 확인시 vagrant이기 때문에 안되나?
vagrant@ubuntu-bionic:/home/qtumai/jason$ sudo mount -t cifs //192.168.0.12/homes ./nas
Password for root@//192.168.0.12/homes:  **********
mount error(13): Permission denied
Refer to the mount.cifs(8) manual page (e.g. man mount.cifs)

# 사용자계정을 지정하니 접속됨
vagrant@ubuntu-bionic:/home/qtumai/jason$ sudo mount -t cifs //192.168.0.12/homes ./nas -o username=사용자계정명
Password for admin@//192.168.0.12/homes:  **********

# 드라이브 마운트 확인
vagrant@ubuntu-bionic:/home/qtumai/jason$ df -h
Filesystem            Size  Used Avail Use% Mounted on
...
//192.168.0.12/homes   11T  7.7T  2.9T  73% /home/qtumai/jason/nas

# 다만, 위의 방법으로는 한번만 마운트되어 접속시마다 해줘야함
```