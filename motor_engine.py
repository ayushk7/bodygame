import math
from tkinter.messagebox import NO
from typing import List
from matplotlib.pyplot import pink
import pyautogui

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
MULT_FACTOR = 4100

GUN_ENGAGE_ANGLE = 200

ORIGIN = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]


# class gun_stat:
#     def _init_(self):
#         self.prev_wrist
#         self.prev_tip
#         self.curr_wrist
#         self.curr_tip


def move_to(point):
    try:

        if 0 <= point[0] <= SCREEN_WIDTH and 0 <= point[1] <= SCREEN_HEIGHT:


            pyautogui.moveTo(point[0], point[1])
            print("Point", point)
            pass

        else:
            
            pyautogui.moveTo(ORIGIN)
            print("was not in range so made it to center {{{{{{{{{{{{}}}}}}}}}}}}}")

    except:
        return False

    return True


def find_quadr(dest, source):
    dx = dest[0] - source[0]
    dy = dest[1] - source[1]

    if dx > 0:
        if dy > 0:
            return 1
        else:
            return 4

    else:

        if dy > 0:
            return 2
        else:
            return 3


def find_angle(tan_theta, quadr):
    # 0.5773502691896258

    if quadr == 1:
        return math.atan(tan_theta)

    elif quadr == 2:
        return math.radians(180 + math.degrees(math.atan(tan_theta)))

    elif quadr == 3:
        return math.radians(180 + math.degrees(math.atan(tan_theta)))

    else:
        return math.radians(360 + math.degrees(math.atan(tan_theta)))


def get_position(angle, distance):
    gun_at_screen = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
    mult_factor = MULT_FACTOR

    gun_at_screen[0] -= distance * math.cos(angle) * mult_factor

    gun_at_screen[1] += distance * math.sin(angle) * mult_factor

    return gun_at_screen


def get_distance(x1, y1, x2, y2):
    # Calculating distance
    return math.sqrt(math.pow(x2 - x1, 2) +
                     math.pow(y2 - y1, 2) * 1.0)


def gun_logic(gun_stat):
    if gun_stat.prev_tip is None or gun_stat.curr_tip is None:
        return 'NOCHANGE'

    # print(type(gun_stat.prev_wrist))

    if isinstance(gun_stat.prev_tip, List):
        return 'NOCHANGE'

    # print(gun_stat.prev_tip)
    # making into lists
    # gun_stat.prev_tip = [gun_stat.prev_tip.x, gun_stat.prev_tip.y]
    # gun_stat.prev_wrist = [gun_stat.prev_wrist.x, gun_stat.prev_wrist.y]
    gun_stat.curr_tip = [gun_stat.curr_tip.x, gun_stat.curr_tip.y]
    gun_stat.curr_wrist = [gun_stat.curr_wrist.x, gun_stat.curr_wrist.y]

    # prev_angle = math.degrees(
    #     find_angle((gun_stat.prev_tip[1] - gun_stat.prev_wrist[1]) / (gun_stat.prev_tip[0] - gun_stat.prev_wrist[0]),
    #                find_quadr(gun_stat.prev_tip, gun_stat.prev_wrist)))
    current_angle = math.degrees(
        find_angle((gun_stat.curr_tip[1] - gun_stat.curr_wrist[1]) / (gun_stat.curr_tip[0] - gun_stat.curr_wrist[0]),
                   find_quadr(gun_stat.curr_tip, gun_stat.curr_wrist)))

    prev_engage = gun_stat.prev_engage
    current_engage = current_angle < GUN_ENGAGE_ANGLE

    print("PREVIOUS CONDITION", gun_stat.prev_engage, "CURRENT ANGLE", current_angle)

    if prev_engage is True and current_engage is False:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>DISENGAGE")
        # pyautogui.mouseUp()
        return 'DISENGAGE'

    if prev_engage is False and current_engage is True:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ENGAGE")
        # pyautogui.mouseDown()
        return 'ENGAGE'

    return 'NOCHANGE'


def controller(landmarks, gun_stat):
    # find all the landmarks
    left_shoulder = [landmarks[0].x, landmarks[0].y]
    right_shoulder = [landmarks[1].x, landmarks[1].y]
    gun = [landmarks[2].x, landmarks[2].y]

    # print("Previous wrist", gun_stat.prev_wrist)
    # if gun_stat.prev_wrist is not None and gun_stat.curr_wrist is not None:
    #     gun_stat.prev_wrist = [gun_stat.prev_wrist.x, gun_stat.prev_wrist.y]
    #     gun_stat.curr_wrist = [gun_stat.curr_wrist.x, gun_stat.curr_wrist.y]

    # gun_stat
    # wrist = gun_stat[0]
    # tip = gun_stat[1]

    neck_center = [None, None]

    neck_center[0] = (left_shoulder[0] + right_shoulder[1]) / 2
    neck_center[1] = (right_shoulder[0] + left_shoulder[1]) / 2

    distance = get_distance(neck_center[0], neck_center[1], gun[0], gun[1])

    # find angle
    tan_theta = (gun[1] - neck_center[1]) / (gun[0] - neck_center[0])

    angle = find_angle(tan_theta, find_quadr(gun, neck_center))

    gun_at_screen = get_position(angle, distance)

    replies = []

    replies.append(move_to(gun_at_screen))
    replies.append(gun_logic(gun_stat))

    return replies