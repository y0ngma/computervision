# docker
wget -qO- https://get.docker.com/ | sh
usermod -aG docker vagrant
echo "다음처럼 쌍따옴표는 역슬레쉬로 표현\"도커설치\"! I am provisioning my quest."
date > /etc/vagrant_provisioned_at

### 나스설정 : 최초 실행이 아닐때 다음을 주석 ###############################################
# 1. 시작할때 자동으로 마운트 시켜주기 위해선 fstab파일을 수정해야한다
cat >> /etc/fstab <<EOL
# [//ip주소/나머지src경로] [로컬dst경로] cifs credentials=[/비번파일경로] 
//192.168.0.12/homes/ /home/nas cifs credentials=/home/.naspassword,rw 0 0
EOL
echo "/etc/fstab 수정"

# 2. '마운트시킬 NAS 경로'와 '로컬에서 해당 경로의 파일을 확인할수 있는 destination 경로'를 생성한다
mkdir -p /home/nas
echo "NAS접근용 폴더 생성"

# 3. 비밀번호 파일생성(파일명무관) 및 접속할 계정정보 입력
cat >> /home/.naspassword <<EOL
username=사용자이름
password=비밀번호
EOL
echo "NAS계정정보 키생성"

# 4. 최초실행시 수동 드라이브 마운트
sudo mount --all
echo "마운트"
#################################################################################