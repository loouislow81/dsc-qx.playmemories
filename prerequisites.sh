#!/bin/bash

function runas_root() {
  # check if sudo
  if [ "$(whoami &2> /dev/null)" != "root" ] &&
     [ "$(id -un &2> /dev/null)" != "root" ]
    then
      echo -e "$title permission denied"
      exit 1
  fi
}

function prerequisites(){
  echo "[dsc-qx] installing packages..."
  apt install -y
    python-qt4
}

######## init
runas_root
prerequisites
