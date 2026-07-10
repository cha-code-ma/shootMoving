from enum import Enum

class turningStatus(Enum):
    LEFT = 1
    STRAIGHT = 0
    RIGHT = -1

class walkingStatus(Enum):
    FORWARD = 1
    STANDING = 0
    BACKWARD = -1
