import cv2
import mediapipe as mp
import math

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

stream = cv2.VideoCapture(1)

if not stream.isOpened():
    print("no stream")
    exit()

count = 0
while(True):
    ret, frame = stream.read()
    #cv2.imwrite("frame%d.jpg" % count, frame)
    if not ret:
        print("no more stream")
        break

    results = pose.process(frame)
    landmarks = results.pose_landmarks

    if landmarks:
   # Extract key landmarks for the hips and shoulders
        left_hip = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
        left_shoulder = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        hip_to_shoulder_vector = [right_shoulder.x - left_hip.x, right_shoulder.y - left_hip.y, right_shoulder.z - left_hip.z]

        angle_with_upward = math.degrees(math.acos(hip_to_shoulder_vector[1] / math.sqrt(sum(x**2 for x in hip_to_shoulder_vector))))
        cv2.putText(frame, f"Angle: {angle_with_upward:.2f} degrees", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        if angle_with_upward < 70:
            cv2.putText(frame, "Collapsed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        for landmark in landmarks.landmark:
            height, width, _ = frame.shape
            cx, cy = int(landmark.x * width), int(landmark.y * height)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
    
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) == ord('q'):
        break
    count += 1


stream.release()
cv2.destroyAllWindows()
    