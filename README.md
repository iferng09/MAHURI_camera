# MAHURI_camera

Camera node for MAHURI Android app.

## Clonning the repository
```bash
git clone https://github.com/iferng09/MAHURI_camera
cd MAHURI_camera/camera_node
```

## Running camera_node and sendImage nodes:

Open two terminals:

**Terminal 1:** Run camera node:
```bash
source /opt/ros/foxy/setup.bash
python3 camera_node.py
```

**Terminal 2:** Run java program which sends the image to MAHURI app:
```bash
java sendImage
```
