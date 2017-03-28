#!/bin/bash

if [ -f /etc/redhat-release ]; then
  echo "EL Distro detected, going to install needed system libs from yum"
  sudo yum -y install \
    ImageMagick \
    ImageMagick-devel \
    libtiff-devel \
    libjpeg-turbo-devel \
    freetype-devel \
    tcl-devel \
    tk-devel \
    libxslt-devel \
    libxml2-devel
fi

IS_OSX=`uname | grep Darwin`
if [ $IS_OSX == "Darwin" ]; then
  OSX_PKGS="libjpeg"
  echo "OSX detected, going to brew install."
  brew install $OSX_PKGS
  if [ $? -ne 0 ]; then
    echo "brew install failed: "
    echo "please verify package name $OSX_PKGS" 
    echo "and make sure homebrew is installed"
    exit 1;
  fi
  echo "System requirements installed"
fi

