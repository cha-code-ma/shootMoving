from enum import Enum

AMOUNT_OF_CHECKS = 3

class turningStatus(Enum):
    LEFT = 1
    STRAIGHT = 0
    RIGHT = -1

class walkingStatus(Enum):
    FORWARD = 1
    STANDING = 0
    BACKWARD = -1

class actionStatus(Enum):
    IDLE = 0
    SHOOTING = 1
    WALKING = 2
    TURNING = 3
