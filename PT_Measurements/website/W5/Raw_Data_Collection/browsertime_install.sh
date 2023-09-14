curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
nvm install node

  
apt-get update -y && apt-get install -y imagemagick libjpeg-dev python3 python3-dev python3-pip python-is-python3 xz-utils wget ca-certificates build-essential --no-install-recommends
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools
python3 -m pip install pyssim OpenCV-Python Numpy image
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar --strip-components 1 -C /usr/bin -xf ffmpeg-release-amd64-static.tar.xz --wildcards ffmpeg*/ff* && rm ffmpeg-release-amd64-static.tar.xz

npm install browsertime -g

