from dataclasses import dataclass
from typing import List
import random
import string
import math
import numpy as np


@dataclass
class Player:
    name: str
    elo: int

@dataclass
class BallHit:    
    position: List[float]
    velocity: List[float]
    rotation: List[float]

@dataclass
class ReplayDirection:
    horizontalAngle: float
    verticalAngle: float

@dataclass
class ReplaySpin:
    topBottom: float
    leftRight: float
    screw: float
    
@dataclass
class BallReplay:
    name: str
    id: str
    position: List[float]
    direction: ReplayDirection
    spin: ReplaySpin
    speedAndRate: float
    

def calculate_angles(vx, vy, vz):
    # Calculate horizontal angle (angle with respect to x-axis)
    horizontal_angle = math.atan2(vy, vx)  # Result in radians
    horizontal_angle_deg = math.degrees(horizontal_angle)  # Convert to degrees

    # Calculate vertical angle (angle with respect to z-axis)
    vertical_angle = math.atan2(vz, math.sqrt(vx**2 + vy**2))  # Result in radians
    vertical_angle_deg = math.degrees(vertical_angle)  # Convert to degrees

    return horizontal_angle_deg, vertical_angle_deg

def calculate_spin_rates(rx, ry, rz):
    # Convert rotation vector components from degrees per second to radians per second
    rx_rad_per_sec = math.radians(rx)
    ry_rad_per_sec = math.radians(ry)
    rz_rad_per_sec = math.radians(rz)

    # Calculate spin rates along topBottom and leftRight axes
    spin_rate_top_bottom = rz_rad_per_sec / (2 * math.pi)
    spin_rate_left_right = ry_rad_per_sec / (2 * math.pi)

    return spin_rate_top_bottom, spin_rate_left_right


def generate_id(size: int = 6) -> str:
    return ''.join(random.choice(string.ascii_letters.capitalize()) for _ in range(size))

def read_game_log(file_path: str):
    with open(file_path, "r") as f:
        for line in f:
            return ""

def convert_ball_hit_to_reply(name: str, ball_hit: BallHit) -> BallReplay:
    horizontal_angle, vertical_angle = calculate_angles(ball_hit.velocity[0], ball_hit.velocity[1], ball_hit.velocity[2])
    calculate_spin_rates(ball_hit.rotation[0], ball_hit.rotation[1], ball_hit.rotation[2])
    return BallReplay(
        name=name,
        id=generate_id(),
        position=ball_hit.position,
        direction=ReplayDirection(horizontalAngle=horizontal_angle, verticalAngle=vertical_angle),
        spin=ReplaySpin(topBottom=0, leftRight=0, screw=0),
        speedAndRate=0)

#def parse_game_logic(log: str):
    

if __name__ == "__main__":
    read_game_log("file")
