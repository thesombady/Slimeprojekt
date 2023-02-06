from PIL import Image
import os
import random
from dataclasses import dataclass
from math import sin, cos


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
    

class Color:
    
    def __init__(self, r: int = 255, g: int = 255, b: int = 255):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)
    
    def __radd__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)
    
    def __sub__(self, other):
        return Color(self.r - other.r, self.g - other.g, self.b - other.b)
    
    def __rsub__(self, other):
        return Color(self.r - other.r, self.g - other.g, self.b - other.b)

    def __mul__(self, other):
        return Color(round(self.r * other), round(self.g * other), round(self.b * other))

    def __rmul__(self, other):
        return Color(round(self.r * other), round(self.g * other), round(self.b * other))
    

@dataclass
class Trail:
    position: vector
    color: Color
    


class Agent:

    def __init__(self, position: vector, angle: float):
        self.position = position
        self.angle = angle
        self.color = Color()
        self.trail = []

    def _updateTrail(self):
        for trail in self.trail:
            trail.color = trail.color - Color(5, 5, 5)
            if trail.color.r <= 0 or trail.color.g <= 0 or trail.color.b <= 0:
                self.trail.remove(trail)


def draw(agents, width, height, n):
    with Image.new("RGB", (width, height), "black") as img:
        for agent in agents:
            nw = agent.position
            img.putpixel((int(agent.position.x), int(agent.position.y)), (255, 255, 255)) # Can move outside the second for loop
            for trail in agent.trail:
                img.putpixel((int(trail.position.x), int(trail.position.y)), (trail.color.r, trail.color.g, trail.color.b))
        # implement a blur system
        img.save(f"Frames\\slime{n}.png")


def sense(agent: Agent, agents: list, sensorAngleOffset: float, width: int, height: int):
    Sensoroffsetdistance = 3
    sensorsize = 5
    sensorangle = agent.angle + sensorAngleOffset
    sensorDirection = vector(cos(sensorangle), sin(sensorangle))
    sensorCenter = agent.position + sensorDirection * Sensoroffsetdistance
    temp = 0
    for tempagent in agents:
        if tempagent == agent:
            pass
        for trailpos in tempagent.trail:
            pos = (trailpos.position - sensorCenter).round # distance between trail and sensor
            if pos.x < sensorsize and pos.y < sensorsize:
                temp += sum(pos)
            else:
                temp += 0
    #print(temp)
    return temp





def Start(width = 500, height = 500, n_agents = 10, NumOfFrames = 300):
    step = 1
    delta = 0.01
    turnspeed = 0.5
    agents = [Agent(position = vector(random.randint(0, width), random.randint(0, height)), angle = random.uniform(0, 360)) for _ in range(n_agents)]
    def update(agentser, width, height, i, step = 25):
            for agent in agentser:
                weightForward = sense(agent, agents, 0, width, height)
                weightLeft = sense(agent, agents, 45, width, height)
                weightRight = sense(agent, agents, -45, width, height)
                randomSteerStrenght = random.uniform(0, 3)
                print(randomSteerStrenght)
                if weightForward > weightLeft and weightForward > weightRight: # continue forward
                    agent.angle += 0
                    print("forward")
                elif weightLeft > weightForward and weightLeft > weightRight: # turn randomly
                    agent.angle += (randomSteerStrenght - 0.5) * 2 * delta * turnspeed
                    print("random")
                elif weightRight > weightLeft:
                    agent.angle -= (randomSteerStrenght ) * delta * turnspeed
                    print("right")
                elif weightRight < weightLeft:
                    agent.angle += (randomSteerStrenght ) * delta * turnspeed
                    print("left")
                newpos: vector = agent.position + (vector(step, 0) * cos(agent.angle) + vector(0, step) * sin(agent.angle)) * delta
                if newpos.x < 0 or newpos.x >= width - 1 or newpos.y < 0 or newpos.y >= height - 1:
                    newpos.x = min(width - 1, max(0, newpos.x))
                    newpos.y = min(height - 1, max(0, newpos.y))
                    agent.angle = random.uniform(0, 360)
                agent.trail.append(Trail(agent.position, agent.color))
                agent.position = newpos.round
                agent._updateTrail()
            draw(agents, width, height, i)
    for i in range(NumOfFrames):
        update(agents, width, height, i, NumOfFrames)
    



if __name__ == "__main__":
    Start()