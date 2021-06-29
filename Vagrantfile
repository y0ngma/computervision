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
  
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  config.vm.provider "virtualbox" do |machine|
    machine.memory = "4096"
    machine.cpus   = 4
  end

  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
  # $script = <<-SCRIPT
  # wget -qO- https://get.docker.com/ | sh
  # usermod -aG docker vagrant

  # echo "다음처럼 쌍따옴표는 역슬레쉬로 표현\"헬로우월드\"! I am provisioning my quest."
  # date > /etc/vagrant_provisioned_at
  # SCRIPT
  $script2 = <<-'SCRIPT'
  echo "다음처럼 쌍따옴표는 역슬레쉬로 표현\"헬로우월드\"! I am provisioning my quest."
  date > /etc/vagrant_provisioned_at
  SCRIPT
  # config.vm.provision "shell", inline: $script
  config.vm.provision "shell", inline: $script2
end
