#!/bin/bash

# Install required packages for automation
pip install selenium==3.141.0 pytest==4.6.9 pandas==0.24.2

# Clone automation codes repository
git clone git://github.com/hisyamuddin-jamirun/tests.git
echo $PASSWORD | sudo -S chmod -R 777 tests

# Export automation library
export PYTHONPATH=$HOME/tests/lib

# Setup Firefox browser and its webdriver
tar -C /opt -xjvf tests/docker/packages/firefox*.tar.bz2
PATH=/opt/firefox:$PATH
export PATH

cp tests/docker/packages/geckodriver /usr/bin
echo $PASSWORD | sudo -S chmod 755 /usr/bin/geckodriver

# Setup Display
Xvfb :1 -screen 0 1920x1080x16 2>/dev/null 1>&2 &
DISPLAY=:1.0
export DISPLAY

# Execute automation
py.test -s tests/projects/ommohome/test_product.py

