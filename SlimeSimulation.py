

import numpy as np
from dataclasses import dataclass
import os
from PIL import Image, ImageDraw


WIDTH = 500
HEIGHT = 500
NAGENTS = 10
DELTA = 0.1
PATH = os.path.join(os.getcwd(), "frames")

class vec:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "vector ({}, {})".format(self.x, self.y)
    
    def __add__(self, other):
        return vec(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return vec(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return vec(self.x * scalar, self.y * scalar)

    @property
    def round(self):
        return vec(round(self.x), round(self.y))

@dataclass
class Agent:
    pos: vec
    angle: float


ALLAGENTS = [Agent(vec(199, 200), -1), Agent(vec(200, 199), 1)]
trail_map = np.zeros((WIDTH, HEIGHT), int)


def render(index: int):
    with Image.new("L", (WIDTH, HEIGHT), "black") as img:
        img = Image.fromarray(np.uint8(trail_map))
        img.save(os.path.join(PATH, "frame{}.png".format(index)))

def sense(agent: Agent, sensorAngleOffset: float):
    sensorSize = 5
    sensorAngle = agent.angle + sensorAngleOffset
    sensorDirection = vec(np.cos(sensorAngle), np.sin(sensorAngle))
    sensorCenter = (agent.pos + sensorDirection * sensorSize).round
    temp = 0
    for i in range(-sensorSize, sensorSize + 1):
        for j in range(-sensorSize, sensorSize + 1):
            x = min(WIDTH - 1, max(0, sensorCenter.x + i))
            y = min(HEIGHT - 1, max(0, sensorCenter.y + j))
            temp += trail_map[round(x)][round(y)]
    return temp 


    
def update(run: int):
    trail_map[trail_map > 0] -= 5
    turnspeed = 0.5
    for agent in ALLAGENTS:
        posX, posY = round(agent.pos.x), round(agent.pos.y)
        trail_map[posX][posY] = 255
        agent.pos = agent.pos + vec(np.cos(agent.angle), np.sin(agent.angle)) * DELTA
        weightForward = sense(agent, 0)
        weightLeft = sense(agent, 45)
        weightRight = sense(agent, -45)
        randomSteerStrenght = np.random.uniform(0, 3)
        if weightForward > weightLeft and weightForward > weightRight: # continue forward
            agent.angle += 0
            print("forward")
        elif weightLeft > weightForward and weightLeft > weightRight: # turn randomly
            agent.angle += (randomSteerStrenght - 0.5) * 2 * DELTA * turnspeed
            print("random")
        elif weightRight > weightLeft:
            agent.angle -= (randomSteerStrenght ) * DELTA * turnspeed
            print("right")
        elif weightRight < weightLeft:
            agent.angle += (randomSteerStrenght ) * DELTA * turnspeed
            print("left")        
        print(weightForward, weightLeft, weightRight)
        if agent.pos.x < 0 or agent.pos.x >= WIDTH or agent.pos.y < 0 or agent.pos.y >= HEIGHT:
            agent.pos.x = min(0, max(HEIGHT - 1, agent.pos.x))
            agent.pos.y = min(0, max(HEIGHT - 1, agent.pos.y))
            agent.angle = np.random.uniform(0, 360)
    render(run)

for i in range(100):
    update(i + 1)

