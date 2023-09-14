#!/bin/bash

cd /root/

apt-get install xvfb -y 
pip3 install xvfbwrapper
pip3 install selenium
pip3 install webdriver-manager
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install ./google-chrome-stable_current_amd64.deb -y
chown -R root selenium_testing/
cp selenium_testing/chromedriver /usr/bin/
