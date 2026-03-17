# Pose TF Broadcaster with MediaPipe and ROS 2

This project uses **MediaPipe Pose** to detect human body landmarks from a webcam feed and publishes selected points as **TF transforms** in **ROS 2**.

---

## Overview
This ROS 2 node captures frames from a webcam, processes them with MediaPipe Pose, and broadcasts selected body landmarks as TF frames.

Currently, the following landmarks are published:
- `head_link`
- `left_hand_link`
- `right_hand_link`

Parent frame:
- `base_link`

> Note: In MediaPipe, landmark `0` corresponds more closely to the **nose** than the full head.  
> Also, landmarks `15` and `16` correspond to the **left wrist** and **right wrist**.  
> The frame names used here are simplified for visualization purposes.

---

## Features
- Real-time webcam capture
- Human pose estimation using MediaPipe
- TF broadcasting in ROS 2
- Easy visualization with RViz
- Simple and lightweight structure for experimentation

---

## Technologies Used
- **Python**
- **ROS 2**
- **MediaPipe**
- **OpenCV**
- **tf2_ros**
- **geometry_msgs**
- **rclpy**

---

## How It Works
1. The webcam captures live video frames.
2. MediaPipe Pose detects human body landmarks.
3. Selected landmarks are converted into ROS-compatible coordinates.
4. These points are published as TF transforms relative to `base_link`.

---

## Coordinate Mapping
MediaPipe provides normalized coordinates in the range of approximately `0-1`.  
These values are transformed into a ROS coordinate system using a simple scaling method.

Current conversion:
- `x = (lm.x - 0.5) * scale`
- `y = (0.5 - lm.y) * scale`
- `z = -lm.z * scale`

This is a basic mapping intended for visualization and experimentation.  
For real-world robotic applications, additional calibration may be required.

---

## Requirements
Make sure the following are installed:

- ROS 2
- Python 3
- OpenCV
- MediaPipe

ROS 2 Python packages:
- `rclpy`
- `tf2_ros`
- `geometry_msgs`

---

## Run

This project currently includes the main Python script for the ROS 2 node.

After integrating it into a ROS 2 Python package, you can run it with:

```bash
ros2 run pose_tf pose_tf_broadcaster
