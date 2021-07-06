Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.box_version = "20210508.0.0"
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
  # config.vm.network "private_network", ip: "192.168.33.10"
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"
  
  config.vm.provider "virtualbox" do |machine|
    machine.gui    = false
    machine.memory = "4096"
    machine.cpus   = 4
  end

  # 작성 문법 예시
  config.vm.provision "shell", inline: "echo Hello, World 한줄"
  config.vm.provision "shell", inline: <<-SHELL
    echo "여러줄 삽입가능형태"
  SHELL
  $script = <<-'SCRIPT'
  echo "다음처럼 쌍따옴표는 역슬레쉬로 표현\"헬로우월드\"! I am provisioning my quest."
  date > /etc/vagrant_provisioned_at
  SCRIPT
  config.vm.provision "shell", inline: $script

  # # NAS synology 마운트 최초 한번만 실행
  # config.vm.provision "shell", path: "nas_mount.sh"
  
  # config.vm.provision "shell", path: "bootstrap.sh"

end
