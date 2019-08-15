#!/bin/bash

runas_root() {
  # check if sudo
  if [ "$(whoami &2> /dev/null)" != "root" ] &&
     [ "$(id -un &2> /dev/null)" != "root" ]; then
      echo -e "[playmemories] permission denied!"
      exit 1
  fi
}

prerequisites(){
  echo "[playmemories] installing packages..."
  apt install -y \
    python-qt4
}

######## init
runas_root
prerequisites
