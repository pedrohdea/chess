python3.9 -m venv venv
pip install --upgrade pip
. venv/bin/activate
pip install -r requirements.txt
sudo apt install v4l-utils
pip install onnxruntime opencv-python numpy
pip install onnxruntime-openvino
pip install pyserial

export QT_QPA_PLATFORM=xcb
