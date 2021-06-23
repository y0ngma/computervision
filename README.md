# 접속정보
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