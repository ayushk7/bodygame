import math


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

ORIGIN = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]


def move_to(point):

    try:
        # pyautogui.MoveTo(point)
        pass
    except:
        return False

    return True


def find_quadr(dest, source):



def find_angle(tan_theta, quadr):



    return 0


def get_position(angle, distance):

    gun_at_screen = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
    mult_factor = 100

    gun_at_screen[0] += distance * math.cos(angle) * mult_factor

    gun_at_screen[1] += distance * math.sin(angle) * mult_factor

    return gun_at_screen


def get_distance(x1, y1, x2, y2):
    # Calculating distance
    return math.sqrt(math.pow(x2 - x1, 2) +
                     math.pow(y2 - y1, 2) * 1.0)


def controller(landmarks):

    # find all the landmarks
    left_shoulder = landmarks[0]
    right_shoulder = landmarks[1]
    gun = landmarks[2]

    neck_center = [None, None]

    neck_center[0] = (left_shoulder[0] + right_shoulder[1])/2
    neck_center[1] = (right_shoulder[0] + left_shoulder[1])/2

    distance = get_distance(neck_center[0], neck_center[1], gun[0], gun[1])

    # find angle
    tan_theta = (gun[1] - neck_center[1])/(gun[0] - neck_center[0])

    angle = find_angle(tan_theta)

    gun_at_screen = get_position(angle, distance)

    return move_to(gun_at_screen)











