# python3.8 기준으로 설치가 되어야 하는데 우분투 기본 python3.6으로 설치됨
sudo apt install python3.8
sudo apt-get install python3-pip
# sudo -H pip3 install --upgrade --force-reinstall numpy 
sudo apt-get install python3-pandas


###################################################################
# 소스에서 최신 OpenCV 버전을 설치하려면 다음 단계를 수행합니다.
# 01. 필요한 종속성을 설치합니다.
sudo apt install build-essential cmake git pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev python3-numpy \
    libtbb2 libtbb-dev libdc1394-22-dev
 
# 02. OpenCV 및 OpenCV 기여 저장소를 복제합니다.
mkdir ~/opencv_build && cd ~/opencv_build
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
# github 저장소의 기본 버전은 버전 4.2.0이었습니다. 이전 버전의 OpenCV를 설치하려면 opencv, opencv_contrib 디렉토리에 이동해 git checkout <opencv-version>을 실행합니다.

# 03. 다운로드가 완료되면 임시 빌드 디렉토리를 만들고 다음으로 전환합니다.
cd ~/opencv_build/opencv
mkdir build && cd build
# CMake로 OpenCV 빌드를 설정합니다.
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
    -D BUILD_EXAMPLES=ON ..

# 04. 컴파일 프로세스를 시작합니다
# 프로세서에 따라 -j 플래그를 수정합니다. 프로세서의 코어 수를 모르는 경우 nproc를 입력하여 찾을 수 있습니다.
make -j4

# 05. 다음을 사용하여 OpenCV를 설치합니다.
sudo make install

# 06. OpenCV가 성공적으로 설치되었는지 확인하려면 다음 명령을 입력하면 OpenCV 버전이 표시됩니다.
pkg-config --modversion opencv4
# 4.2.0
python3 -c "import cv2; print(cv2.__version__)"
# 4.2.0-dev
###################################################################
