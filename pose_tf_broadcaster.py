import cv2
import mediapipe as mp
import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from tf2_ros import TransformBroadcaster


class PoseTfBroadcaster(Node):
    """
    ROS 2 node that captures webcam input, estimates human pose using MediaPipe,
    and broadcasts selected landmarks as TF transforms.
    """

    def __init__(self):
        super().__init__("pose_tf_broadcaster")

        self.br = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.broadcast_transforms)

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()

        self.cap = cv2.VideoCapture(0)

        # Scale factor to map MediaPipe normalized coordinates into ROS space
        self.scale = 1.0

        self.base_frame = "base_link"

        self.get_logger().info("Pose TF Broadcaster node has started.")

    def create_transform(self, landmark_id, child_frame, results):
        """
        Create a TransformStamped message for a given MediaPipe landmark.
        """
        lm = results.pose_landmarks.landmark[landmark_id]

        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = self.base_frame
        transform.child_frame_id = child_frame

        # Convert MediaPipe normalized coordinates into ROS-compatible coordinates
        transform.transform.translation.x = (lm.x - 0.5) * self.scale
        transform.transform.translation.y = (0.5 - lm.y) * self.scale
        transform.transform.translation.z = -lm.z * self.scale

        # No rotation is estimated in this version
        transform.transform.rotation.x = 0.0
        transform.transform.rotation.y = 0.0
        transform.transform.rotation.z = 0.0
        transform.transform.rotation.w = 1.0

        return transform

    def broadcast_transforms(self):
        """
        Capture frame from webcam, run pose estimation, and broadcast transforms.
        """
        success, frame = self.cap.read()
        if not success:
            self.get_logger().warning("Failed to read frame from camera.")
            return

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        if not results.pose_landmarks:
            return

        # MediaPipe landmark IDs:
        # 0  -> nose/head reference
        # 15 -> left wrist
        # 16 -> right wrist
        head_tf = self.create_transform(0, "head_link", results)
        left_hand_tf = self.create_transform(15, "left_hand_link", results)
        right_hand_tf = self.create_transform(16, "right_hand_link", results)

        self.br.sendTransform(head_tf)
        self.br.sendTransform(left_hand_tf)
        self.br.sendTransform(right_hand_tf)

    def destroy_node(self):
        """
        Release resources before shutting down the node.
        """
        if self.cap.isOpened():
            self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = PoseTfBroadcaster()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
