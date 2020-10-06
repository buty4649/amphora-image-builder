# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false

    vb.memory = "2048"
  end
  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    apt update -qqy && \
    apt install -qqy git sudo
  SHELL
end
