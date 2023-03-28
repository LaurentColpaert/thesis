"""
Laurent Colpaert - Thesis 2022-2023
"""
import ast
from math import cos, exp, sin, sqrt
import os
import subprocess
import time
from xml.dom import minidom
from numpy import linalg as LA


import numpy as np


class Simulation():
    """
    Class Simulation : contain the function necessary to launch an argos simulation based on AutoMoDe
    """
    def __init__(self, argos_file: str = "aac.argos") -> None:
        self.swarm_pos = []
        self.argos_file = argos_file
        self.argos_file = "aac.argos"
        #Besqt PFSM
        self.pfsm = "--fsm-config --nstates 4 --s0 4 --att0 3.25 --n0 2 --n0x0 0 --c0x0 5 --p0x0 0.23 --n0x1 2 --c0x1 0 --p0x1 0.70 --s1 2 --n1 3 --n1x0 0 --c1x0 4 --w1x0 8.91 --p1x0 7 --n1x1 1 --c1x1 0 --p1x1 0.15 --n1x2 2 --c1x2 3 --w1x2 1.68 --p1x2 10 --s2 1 --n2 1 --n2x0 0 --c2x0 3 --w2x0 6.93 --p2x0 4 --s3 4 --att3 3.71 --n3 2 --n3x0 0 --c3x0 1 --p3x0 0.50 --n3x1 2 --c3x1 5 --p3x1 0.62"
        #should be worse fsm
        self.pfsm = "--fsm-config --nstates 4 --s0 4 --att0 1.01 --n0 4 --n0x0 0 --c0x0 3 --w0x0 13.75 --p0x0 1 --n0x1 2 --c0x1 5 --p0x1 0.07 --n0x2 2 --c0x2 5 --p0x2 0.64 --n0x3 2 --c0x3 3 --w0x3 13.22 --p0x3 5 --s1 1 --n1 4 --n1x0 2 --c1x0 2 --p1x0 0.80 --n1x1 1 --c1x1 2 --p1x1 0.53 --n1x2 0 --c1x2 3 --w1x2 5.66 --p1x2 10 --n1x3 0 --c1x3 5 --p1x3 0.12 --s2 2 --n2 2 --n2x0 0 --c2x0 1 --p2x0 0.06 --n2x1 1 --c2x1 1 --p2x1 0.71 --s3 4 --att3 3.92 --n3 3 --n3x0 2 --c3x0 3 --w3x0 5.45 --p3x0 9 --n3x1 1 --c3x1 0 --p3x1 0.98 --n3x2 0 --c3x2 4 --w3x2 9.54 --p3x2 5"
        #test
        self.pfsm = "--fsm-config --nstates 4 --s0 3 --n0 2 --n0x0 2 --c0x0 3 --p0x0 10 --w0x0 0.03 --n0x1 0 --c0x1 4 --p0x1 9 --w0x1 0.03 --s1 1 --s2 1 --n2 3 --n2x0 0 --c2x0 1 --p2x0 0.01 --n2x1 0 --c2x1 0 --p2x1 0.0 --n2x2 0 --c2x2 1 --p2x2 0.01 --s3 2"
        self.arenaD = 3
        self.nRbt = 20
        self.circle_goal = [0,0,0]
        # Patch = [x,y,r]
        self.patches, self.obstacles = self.retrieve_patches()
        
    def read_file(self,filename: str = 'position.txt'):
        """
        Read the value of a file and retrieve all the line into a list

        Args:
            -filename (str): the name of the file 

        Returns:
            -None
        """
        with open(f"/home/laurent/Documents/Polytech/MA2/thesis/examples/argos/{filename}") as f:
            self.swarm_pos.extend(ast.literal_eval(line) for line in f)

        self.swarm_pos = [list(t) for t in self.swarm_pos]
        os.remove(f"/home/laurent/Documents/Polytech/MA2/thesis/examples/argos/{filename}")

    def run_simulation(self)-> tuple:
        """
        Run an argos simulation and compute the behaviour and fitness

        Args:
            -None
        Returns:
            -tuple(float): the value of the behaviour and fitness
        """
        command = f"/home/laurent/AutoMoDe/bin/automode_main -c {self.argos_file} -n {self.pfsm}"
        subprocess.run(f"cd /home/laurent/Documents/Polytech/MA2/thesis/examples/argos; {command}",shell = True)
        
        time.sleep(3)

        self.read_file()
        features = self.compute_features()
        print("Features : ", features)
        fitness = self.compute_fitness()
        print("Fitness : ", fitness)
        return features,fitness

    def compute_features(self)-> float:
        """
        Compute the features of a run 

        Args:
            -None
        Returns:
            -float: the value of the behaviour
        """
        return self.compute_phi()

    def compute_fitness(self)-> int:
        """
        Compute the fitness of a run = the number of epuck inside the white circle

        Args:
            -None
        Returns:
            -int: the value of the fitness
        """
        return sum(
            self.distToCircle(self.circle_goal, pos) < self.circle_goal[2]
            for pos in self.swarm_pos
        )

    def compute_phi(self)-> float:
        """
        Compute the phi behaviour.
        It's the distance of each robot from the landmarks

        Args:
            -None
        Returns:
            -float: the value of the behaviour
        """
        phi_tot = []
        for p in self.patches:
            phi = []
            patch = p.copy()

            for pos in self.swarm_pos:
                if(len(patch) == 3):
                    distance = self.distToCircle(patch, pos)
                else:
                    distance = self.distToRect(patch, pos)
                phi.append(distance)

            h = (2*np.log(10))/(self.arenaD**2)
            phi = [exp(- h * self.arenaD * pos) for pos in phi]
            phi.sort(reverse=True)
            phi_tot.extend(iter(phi))

        phi = []
        for i in range(len(self.swarm_pos)):
            neighbors = self.swarm_pos.copy()
            neighbors.pop(i)
            distance = min(
                LA.norm(np.array(self.swarm_pos[i]) - np.array(n), ord=2)
                for n in neighbors
            )
            phi.append(distance)

        h = (2*np.log(10))/(self.arenaD**2)
        phi = [exp(- h * self.arenaD * pos) for pos in phi]
        phi.sort(reverse=True)

        phi_tot.extend(iter(phi))


        return sum(phi_tot) / len(phi_tot)

    def retrieve_patches(self)->tuple:
        """
        Retrieve the different values of the landmarks inside the argos file

        Args:
            -None
        Returns:
            -tuple: the circles or rectangles and the obstacles
        """
        patches = []

        # parse an xml file by name
        file = minidom.parse(f'/home/laurent/Documents/Polytech/MA2/thesis/examples/argos/{self.argos_file}')

        #retriving circle patches
        circles = file.getElementsByTagName('circle')
        for c in circles:
            if c.getAttribute("color") != "white":
                self.circle_goal = ast.literal_eval("[" + c.getAttribute("position") + "," + c.getAttribute("radius") + "]")
            patches.append(ast.literal_eval("[" + c.getAttribute("position") + "," + c.getAttribute("radius") + "]"))
        #retriving rect patches
        rectangles = file.getElementsByTagName('rectangle')
        for r in rectangles:
            if(r.getAttribute("color") == "white"):
                patches.append(ast.literal_eval("[" + r.getAttribute("center") + "," + r.getAttribute("width") + "," + r.getAttribute("height") + "]"))
            else:
                patches.append(ast.literal_eval("[" + r.getAttribute("center") + "," + r.getAttribute("width") + "," + r.getAttribute("height") + "]"))

        obstacles = []
        boxes = file.getElementsByTagName('box')
        for b in  boxes:
            if("obstacle" in b.getAttribute("id")):
                body = b.getElementsByTagName("body")[0]
                center = ast.literal_eval("[" + body.getAttribute("position") + "]")[:-1]
                width = ast.literal_eval("[" + b.getAttribute("size") + "]")[1]
                orientation = ast.literal_eval("[" + body.getAttribute("orientation") + "]")[0]
                a = [center[0] + width*sin(orientation), center[1] + width*cos(orientation)]
                b = [center[0] - width*sin(orientation), center[1] - width*cos(orientation)]
                obstacles.append([a,b])

        return patches, obstacles   
    
    def distToCircle(self, circle : tuple, pos : tuple)-> float:
        """
        Compute the distance of a point to a circle

        Args:
            -circle (tuple): (x,y,radius)
            -pos (tuple): (x,y) = the position of the point
        Returns:
            -float: the distance
        """
        c_x = circle[0]
        c_y = circle[1]
        r = circle[2]
        for obs in self.obstacles:
            if(self.intersect(pos,circle,obs[0], obs[1])):
                return self.arenaD
        return max(0, sqrt((pos[0]-c_x)**2 + (pos[1] - c_y)**2) - r)

    def distToRect(self, rect : tuple, pos : tuple)-> float:
        """
        Compute the distance of a point to a rectangle

        Args:
            -rect (tuple): (x,y,width,length)
            -pos (tuple): (x,y) = the position of the point
        Returns:
            -float: the distance
        """
        x_min = rect[0] - rect[2]/2
        x_max = rect[0] + rect[2]/2
        y_min = rect[1] - rect[3]/2
        y_max = rect[1] + rect[3]/2

        dx = max(x_min - pos[0], 0, pos[0] - x_max)
        dy = max(y_min - pos[1], 0, pos[1] - y_max)
        
        for obs in self.obstacles:
            if(self.intersect(pos,[x_min,pos[1]],obs[0], obs[1]) or
               self.intersect(pos,[x_max,pos[1]],obs[0], obs[1]) or
               self.intersect(pos,[pos[0],y_min],obs[0], obs[1]) or
               self.intersect(pos,[pos[0],y_max],obs[0], obs[1])):
               return self.arenaD
        return sqrt(dx**2 + dy**2)

    def ccw(self, a : float, b : float, c : float) -> bool:
        """
        Conter-clockwise function
        """
        return (c[0] - a[0])*(b[1] - a[1]) > (b[0] - a[0])*(c[1] - a[1])

    def intersect(self, a : float, b : float, c : float, d : float)-> bool:
        """
        Return true if segments AB and CD intersect

        Args:
            -a (float): the x of the first position
            -b (float): the y of the first position
            -c (float): the x of the second position
            -d (float): the y of the second position
        Returns:
            -bool: intersect or not
        """
        return (self.ccw(a,c,d) != self.ccw(b,c,d)) and (self.ccw(a,b,c) != self.ccw(a,b,d))