to do library installs
# LOCAL
mkdir yolo_packages && cd yolo_packages
pip download ultralytics

scp -r yolo_packages user@remote:/tmp/

# REMOTE
cd /tmp/yolo_packages
pip install *.whl