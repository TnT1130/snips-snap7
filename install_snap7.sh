#!/bin/bash

#not testted


version="snap7-full-1.4.2"
arch="x86_64" #linux
#arch="arm_v7" #pi



p7zipExists=$(command -v p7zip)


if [[ ! -s /usr/lib/libsnap7.so ]]; then
  #download requirements
  if [[ $p7zipExists == "" ]]; then
    if [[ $(command -v apt) != "" ]]; then
      apt install -y p7zip-full
    elif [[  $(command -v pacman) != "" ]]; then
      pacman --noconfirm -S p7zip
    else
      echo "unable to install p7zip"
      exit 1
    fi
  fi
  wget https://netcologne.dl.sourceforge.net/project/snap7/1.4.2/$version.7z
  #p7zip -d $version.7z
  7z x $version.7z
  #build libsnpa7
  cd $version/build/unix
  make -f "$arch"_linux.mk
  #install
  cp ../bin/$arch-linux/libsnap7.so /usr/lib
  ldconfig /usr/lib/libsnap7.so
  #cleanup
  cd ../../../
  rm -r $version/
  rm $version.7z
  if [[ $p7zipExists == "" ]]; then
    if [[ $(command -v apt) != "" ]]; then
      apt autoremove -y p7zip-full
    elif [[  $(command -v pacman) != "" ]]; then
      pacman --noconfirm -Rs p7zip
    fi
  fi
fi
exit 0