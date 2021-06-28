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
### 에러로그
```s
# 마운트할 폴더 생성
vagrant@ubuntu-bionic:/home$ sudo mkdir -p qtumai/jason/nas/
vagrant@ubuntu-bionic:/home$ cd qtumai/jason/

# 잘못된 문법
vagrant@ubuntu-bionic:/home/qtumai/jason$ sudo mount -t cifs 192.168.0.12:/homes ./nas
mount.cifs: bad UNC (192.168.0.12:/homes)

# who am i 확인하면 사용자가 vagrant이기 때문에 안되나?
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
udev                  2.0G     0  2.0G   0% /dev
tmpfs                 395M  656K  394M   1% /run
/dev/sda1              39G  2.1G   37G   6% /
tmpfs                 2.0G     0  2.0G   0% /dev/shm
tmpfs                 5.0M     0  5.0M   0% /run/lock
tmpfs                 2.0G     0  2.0G   0% /sys/fs/cgroup
vagrant               477G  145G  332G  31% /vagrant
tmpfs                 395M     0  395M   0% /run/user/1000
//192.168.0.12/homes   11T  7.7T  2.9T  73% /home/qtumai/jason/nas

```

