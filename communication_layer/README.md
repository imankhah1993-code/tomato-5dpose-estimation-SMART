# Tomato 5D Pose Estimation ROS 2 Package

## Overview

This project provides a ROS 2 based tomato perception pipeline using:

* **StereoLabs ZED stereo camera**
* **YOLO keypoint detection**
* **3D point cloud geometry**
* **Tomato orientation estimation**

The system detects tomatoes, estimates their 3D position, calculates geometric properties, and outputs a 5D pose:

```
[X, Y, Z, Yaw, Pitch]
```

where:

| Parameter | Description                  |
| --------- | ---------------------------- |
| X         | Tomato position in meters    |
| Y         | Tomato position in meters    |
| Z         | Tomato depth in meters       |
| Yaw       | Horizontal orientation angle |
| Pitch     | Vertical orientation angle   |

---

# Architecture

The software is separated into independent layers:

```
                 ZED Camera
                     |
                     |
              zed_camera.py
                     |
                     |
              ROS2 Node Layer
              ros_node.py
                     |
        ----------------------------
        |                          |
        v                          v

 detector.py              geometry.py

 YOLO Detection           3D Geometry

        |                          |
        ----------------------------
                     |
                     v

                  pose.py

              5D Pose Estimation

                     |
                     v

             ROS2 Topics/Services
```

---



# Software Layers

## 1. Detection Layer

File:

```
src/detector.py
```

Responsibilities:

* Load YOLO model
* Detect tomatoes
* Extract stem keypoints
* Return:

```
Bounding box
Stem location
```

The detector does not perform any geometry or pose calculations.

---

## 2. Geometry Layer

File:

```
src/geometry.py
```

Responsibilities:

Using:

* YOLO bounding box
* Stem keypoint
* ZED XYZ point cloud

It estimates:

* Tomato center in 3D
* Stem position in 3D
* Orientation reference point
* Tomato diameter estimation

Output:

```
{
 stem3d,
 center3d,
 diameter
}
```

---

## 3. Pose Layer

File:

```
src/pose.py
```

Responsibilities:

Calculates tomato pose from the geometry output.

Output:

```
{
 x,
 y,
 z,
 yaw,
 pitch
}
```

The final tomato pose is:

```
[x, y, z, yaw, pitch]
```

---

# ROS 2 Interfaces

## Published Topics

### Camera visualization

Topic:

```
/tomato/image
```

Message:

```
sensor_msgs/Image
```

Contains:

* YOLO detections
* Keypoints
* Pose visualization

---

# Services

## Next Tomato

Service:

```
/tomato/next
```

Type:

```
std_srvs/Trigger
```

Example:

```bash
ros2 service call /tomato/next std_srvs/srv/Trigger
```

---

## Reset

Service:

```
/tomato/reset
```

Example:

```bash
ros2 service call /tomato/reset std_srvs/srv/Trigger
```

---

# Installation

## 1. Create ROS 2 workspace

```bash
mkdir -p ~/tomato_ws/src

cd ~/tomato_ws/src
```

Clone repository:

```bash
git 
```

Build workspace:

```bash
cd ~/tomato_ws

colcon build
```

Source ROS:

```bash
source install/setup.bash
```

---

# Python Dependencies

Install:

```bash
pip install -r requirements.txt
```

---

# ZED Setup

Install the ZED SDK:

https://www.stereolabs.com/developers/

Verify:

```bash
python3 -c "import pyzed.sl"
```

---

# Model Setup

Place the YOLO model here:

```
models/best.pt
```

The model should contain:

* Tomato detection
* Stem keypoint prediction

---

# Running

Launch the node:

```bash
ros2 run tomato_pose_ros2 main
```

or:

```bash
python3 main.py
```

---

# Example Output

Terminal:

```
X=0.42
Y=-0.11
Z=0.68

Yaw=21.5
Pitch=-7.2

Diameter=0.08m
```

---


# Author
Iman Mirzakhah