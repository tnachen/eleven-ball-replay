from dataclasses import dataclass
from typing import List
import random
import string
import json
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


def calculate_speed_value(velocity):
    return np.linalg.norm(velocity)

def calculate_angles(velocity):
    """
    Prompt:
    given a velocity vector for a ball of x, y, z axis measured in meters per second,
    generate python code that can measure the horizontal and vertical angle the ball is heading to
    """
    # Calculate horizontal angle (angle in xy-plane)
    horizontal_angle = np.arctan2(velocity[1], velocity[0]) # atan2(y, x)

    # Calculate vertical angle (angle in xz-plane)
    vertical_angle = np.arctan2(velocity[2], np.linalg.norm(velocity[:2])) # atan2(z, sqrt(x^2 + y^2))

    # Convert angles to degrees
    horizontal_angle_deg = np.degrees(horizontal_angle)
    vertical_angle_deg = np.degrees(vertical_angle)

    return horizontal_angle_deg, vertical_angle_deg

def calculate_spin_rate(velocity, rotation):
    """
    Prompt:
    given a velocity vector for a ball of x, y, z axis measured in meters per second,
    and a rotation vector in x, y, z axis measured in degrees per second,
    generate python code that can calculate the spin rate of the ball in full rotations per second in both topDown direction
    and leftRight direction relative to the velocity vector direction.
    """
    # Convert rotation vector from degrees per second to radians per second
    rotation_radians = np.radians(rotation)

    # Normalize velocity vector
    velocity_normalized = velocity / np.linalg.norm(velocity)

    # Compute angular velocity vector (cross product of velocity and rotation)
    angular_velocity = np.cross(velocity_normalized, rotation_radians)

    # Calculate spin rate in topDown direction
    topDown_spin_rate = np.linalg.norm(angular_velocity[0]) / (2 * np.pi)

    # Calculate spin rate in leftRight direction
    leftRight_spin_rate = np.linalg.norm(angular_velocity[1]) / (2 * np.pi)

    return topDown_spin_rate, leftRight_spin_rate


def generate_id(size: int = 6) -> str:
    return ''.join(random.choice(string.ascii_letters.capitalize()) for _ in range(size))


def read_game_log(file_path: str):
    with open(file_path, "r") as f:
        for line in f:
            return ""


def convert_ball_hit_to_reply(name: str, ball_hit: BallHit) -> BallReplay:
    horizontal_angle, vertical_angle = calculate_angles(ball_hit.velocity)
    top_bottom, left_right = calculate_spin_rate(ball_hit.velocity, ball_hit.rotation)
    return BallReplay(
        name=name,
        id=generate_id(),
        position=ball_hit.position,
        direction=ReplayDirection(horizontalAngle=horizontal_angle, verticalAngle=vertical_angle),
        spin=ReplaySpin(topBottom=top_bottom, leftRight=left_right, screw=0),
        speedAndRate=calculate_speed_value(ball_hit.velocity))


def add_replays_to_ball_machine(replays: List[BallReplay], ball_settings_file: str):
    new_settings = ""
    with open(ball_settings_file, "r") as f:
        settings = json.loads(f)
        for replay in replays:
            settings["shots"]["data"][replay.id] = {
                "Description":"",
                "isActive":"False",
                "position":{
                    "raw":{
                        "x":"0.00160598754882813",
                        "y":"-0.279831767082214",
                        "z":"-0.0446159839630127"
                    },
                    "spread":{
                        "x":"0",
                        "y":"0",
                        "z":"0"
                    }
                },
                "direction":{
                    "raw":{
                        "horizontalAngle":"0.336875915527344",
                        "verticalAngle":"15.4029006958008"
                    },
                    "spread":{
                        "horizontalAngle":"11.4891128540039",
                        "verticalAngle":"0"
                    }
                    },
                    "spin":{
                    "raw":{
                        "topBottom":"33.3343963623047",
                        "leftRight":"0",
                        "screw":"0"
                    },
                    "spread":{
                        "topBottom":"0",
                        "leftRight":"0",
                        "screw":"0"
                    }
                },
                "speedAndRate":{
                    "raw":{
                        "speed":"8.3076696395874",
                        "secondsPerLaunch":"0.995049715042114",
                        "PostDelay":"0"
                    },
                    "spread":{
                        "speed":"0",
                        "secondsPerLaunch":"0",
                        "PostDelay":"0"
                    }
                },
                "DataName":replay.name,
                "CanUpdate":"True"
            }

        new_settings = json.dumps(settings)

    with open(ball_settings_file, "w") as f:
        f.write(new_settings)

#def parse_game_logic(log: str):


if __name__ == "__main__":
    read_game_log("file")
