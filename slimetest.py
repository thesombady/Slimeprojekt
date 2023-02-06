import numpy as np
from PIL import Image, ImageFilter
import os
from dataclasses import dataclass
import random
from math import sin, cos


WIDTH = 500
HEIGHT = 500
DELTA = 1
signal_map = np.zeros((WIDTH, HEIGHT), int)

class vector:
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y)
    
    def __radd__(self, other):
        return vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return vector(self.x - other.x, self.y - other.y)
    
    def __rsub__(self, other):
        return vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return vector(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        if other != 0:
            return vector(self.x / other, self.y / other)
        raise ZeroDivisionError("Cant divide by zero")
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range")
    
    def __repr__(self) -> str:
        return f"vector({self.x}, {self.y})"
    
    def __sum__(self):
        return self.x + self.y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    @property
    def round(self):
        return vector(round(self.x), round(self.y))

@dataclass
class Agent:
    pos: vector
    angle: float

AGENTS = [Agent(vector(random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)), random.uniform(0, 360)) for _ in range(10)]

def update():
    for agent in AGENTS:
        agent.pos += vector(cos(agent.angle), sin(agent.angle)) * DELTA
        if agent.pos.x < 0 or agent.pos.x >= WIDTH or agent.pos.y < 0 or agent.pos.y >= HEIGHT:
            agent.pos.x = min(WIDTH - 1, max(0, agent.pos.x))
            agent.pos.y = min(HEIGHT - 1, max(0, agent.pos.y))
            agent.angle = random.uniform(0, 360)
        signal_map[int(agent.pos.x), int(agent.pos.y)] = 1



def draw(frame, agents=AGENTS):
    try:
        img = Image.new("RGB", (WIDTH, HEIGHT))
        img.putdata(signal_map.flatten())
        img = img.filter(ImageFilter.GaussianBlur(3))
        pixels = img.load()
        for agent in agents:
            pixels[int(agent.pos.x), int(agent.pos.y)] = (255, 255, 255)
        img.save(os.path.join("images", f"{frame + 1}.png"))
    except Exception as e:
        print(signal_map)
for i in range(10):
    draw(i)
    update()

