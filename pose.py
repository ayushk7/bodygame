# TechVidvan Human pose estimator
# import necessary packages

# from turtle import pos
import cv2
import mediapipe as mp
import time
from motor_engine import controller

class GunStats:
    def __init__(self, curr_w, curr_t, prev_w, prev_t):
        self.curr_wrist = curr_w
        self.curr_tip = curr_t
        self.prev_wrist = prev_w
        self.prev_tip = prev_t
        self.prev_engage = False

LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
RIGHT_INDEX = 20
# initialize Pose estimator
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# create capture object
cap = cv2.VideoCapture(0)
c = 0;


print("Starting M.E.H.K 1")
time.sleep(3)

gun_stat = GunStats(None, None, None, None)

while cap.isOpened():
    # read frame from capture object
        _, frame = cap.read()
        

        
        # convert the frame to RGB format
        RGB = cv2.cvtColor(frame, 
        cv2.COLOR_BGR2RGB)
        # time.sleep(3)
        # process the RGB frame to get the result
        results = pose.process(RGB)
        # print(len(results.pose_landmarks.landmark), results.pose_landmarks.landmark[LEFT_SHOULDER])

        # print("Land marks", results.pose_landmarks)
        if results.pose_landmarks is not None:
            # print("FOUnd landmarks")
            # print("separate\n\n")
            left_shoulder = results.pose_landmarks.landmark[LEFT_SHOULDER]
            right_shoulder = results.pose_landmarks.landmark[RIGHT_SHOULDER]
            left_wrist = results.pose_landmarks.landmark[LEFT_WRIST]
            right_wrist = results.pose_landmarks.landmark[RIGHT_WRIST]
            
            
            # print(left_shoulder, right_shoulder, left_wrist, right_wrist)
            gun_stat.prev_wrist = gun_stat.curr_wrist
            gun_stat.prev_tip = gun_stat.curr_tip
            gun_stat.curr_wrist = results.pose_landmarks.landmark[RIGHT_WRIST]
            gun_stat.curr_tip = results.pose_landmarks.landmark[RIGHT_INDEX]
            engagedStat = controller([left_shoulder, right_shoulder, right_wrist], gun_stat)[1]
            # draw detected skeleton on the frame
            print("Main got", engagedStat)
            if engagedStat == "ENGAGE":
                gun_stat.prev_engage = True
            elif engagedStat == "DISENGAGE":
                gun_stat.prev_engage = False


            print("IN the driver function", gun_stat.prev_engage)
            mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # show the final output
        cv2.imshow('Output', frame)
        # break
        # if c == 32:
            # break
        
    
        if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
