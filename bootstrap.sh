wget -qO- https://get.docker.com/ | sh
usermod -aG docker vagrant
echo "다음처럼 쌍따옴표는 역슬레쉬로 표현\"헬로우월드\"! I am provisioning my quest."
date > /etc/vagrant_provisioned_at
