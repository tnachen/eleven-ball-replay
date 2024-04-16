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
class Game:
    player1: Player
    player2: Player
    winner: Player
    match_sets: List[BallHit]

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


def normalize(v):
    return v / np.linalg.norm(v)


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


def calculate_final_rotation(rotation_vec, velocity_vec):
    """
    Prompt:
    -------
    Given a velocity vector for a ball of x, y, z axis measured in meters per second, and a rotation vector in x, y, z axis measured in degrees per second,
 generate python code that can calculate the spin rate of the ball in full rotations per second in both x, y and z direction along the axis of the velocity vector launch vector.
   One example is rotation vector x=6709.05859375, y=-7512.5166015625,  z=-1004.12396240234 and velocity vector x=0.386714577674866, y=-1.87845945358276, z=-7.34596824645996, 
   and the output should be  final rotation vector x=-18.46387396918403, y=19.2877197265625, z=8.81121080186632
    """
    # Convert rotation from degrees per second to radians per second
    rotation_vec_rad = np.radians(rotation_vec)
    
    # Normalizing the velocity vector to use as the new z-axis
    z_axis = normalize(velocity_vec)
    
    # Arbitrarily choosing the global y-axis to find a perpendicular x-axis
    if np.allclose(z_axis, [0, 1, 0]):
        # If the velocity vector is vertical, use global x-axis instead
        arbitrary_axis = np.array([1, 0, 0])
    else:
        arbitrary_axis = np.array([0, 1, 0])
    
    x_axis = normalize(np.cross(arbitrary_axis, z_axis))
    y_axis = np.cross(z_axis, x_axis)
    
    # Creating rotation matrix from the new basis vectors
    rotation_matrix = np.array([x_axis, y_axis, z_axis]).T
    
    # Transforming the rotation vector to the new coordinate system
    new_rotation_vec_rad = rotation_matrix @ rotation_vec_rad
    
    # Convert radians per second back to degrees per second
    new_rotation_vec_deg = np.degrees(new_rotation_vec_rad)
    
    # Convert from degrees per second to full rotations per second
    final_rotation_vec = new_rotation_vec_deg / 360.0
    
    return final_rotation_vec



def generate_id(size: int = 6) -> str:
    return ''.join(random.choice(string.ascii_letters.capitalize()) for _ in range(size))


def parse_match_events(file_path: str):
    with open(file_path, "r") as f:
        for line in f:
            return ""


def convert_ball_hit_to_reply(name: str, ball_hit: BallHit) -> BallReplay:
    horizontal_angle, vertical_angle = calculate_angles(ball_hit.velocity)
    top_bottom, left_right, screw = calculate_final_rotation(ball_hit.velocity, ball_hit.rotation)
    return BallReplay(
        name=name,
        id=generate_id(),
        position=ball_hit.position,
        direction=ReplayDirection(horizontalAngle=horizontal_angle, verticalAngle=vertical_angle),
        spin=ReplaySpin(topBottom=top_bottom, leftRight=left_right, screw=screw),
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
