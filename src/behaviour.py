"""
Laurent Colpaert - Thesis 2022-2023
"""
from enum import Enum
from math import  exp
import numpy as np
from numpy import linalg as LA

from utility import distToCircle, distToRect

class behaviours(Enum):
    PHI = 1
    DUTY_FACTOR = 2

class Behaviour:
    def __init__(self, b1 : behaviours, b2 : behaviours) -> None:
        self.b1 = b1
        self.range1 = self.set_range(self.b1)
        self.b2 = b2
        self.range2 = self.set_range(self.b1)

    def setup(self,circle_goal, nRbt, iteration,arenaD : float, patches : list,obstacles : list) -> None:
        self.circle_goal = circle_goal
        self.nRbt = nRbt
        self.iteration = iteration
        self.arenaD = arenaD
        self.patches = patches
        self.obstacles = obstacles


    def retrieve_behaviour_fct(self) -> list:
        """
        Retrieve the two behaviour function selected
        """
        return self.get_behaviours(self.b1),self.get_behaviours(self.b2)

    def get_behaviours(self, behaviour : behaviours) -> list:
        """
        Retrieve a behaviour function based on the input behaviour
        """
        if behaviour.value == 1: #DUTY_FACTOR
            return self.duty_factor
        elif behaviour.value == 2: #PHI
            return self.compute_phi
        
    def set_range(self, b : behaviours) -> list: 
        """
        Return the corresponding range depending on the behaviour chosen
        """
        if b.value == 1: #DUTY_FACTOR
            return [0,1]
        elif b.value == 2: #PHI
            return [0,1]
        
    def duty_factor(self,swarm_pos : list)-> float:
        """
        Compute the duty factor.
        It's the amout of time that all the robot have spent in the final landmark

        Args:
            -None
        Returns:
            -float: the value of the behaviour
        """
        return sum(
            distToCircle(self.circle_goal, pos,self.obstacles,self.arenaD) < self.circle_goal[2]
            for pos in swarm_pos[:-20]
        )/(self.nRbt * self.iteration)

    def compute_phi(self, swarm_pos : list)-> float:
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

            for pos in swarm_pos[-self.nRbt:]:
                if(len(patch) == 3):
                    distance = distToCircle(patch, pos,self.obstacles,self.arenaD)
                else:
                    distance = distToRect(patch, pos,self.obstacles,self.arenaD)
                phi.append(distance)

            h = (2*np.log(10))/(self.arenaD**2)
            phi = [exp(- h * self.arenaD * pos) for pos in phi]
            phi.sort(reverse=True)
            phi_tot.extend(iter(phi))

        phi = []
        for i in range(self.nRbt):
            neighbors = swarm_pos[-self.nRbt:].copy()
            neighbors.pop(i)
            distance = min(
                LA.norm(np.array(swarm_pos[-self.nRbt + i]) - np.array(n), ord=2)
                for n in neighbors
            )
            phi.append(distance)

        h = (2*np.log(10))/(self.arenaD**2)
        phi = [exp(- h * self.arenaD * pos) for pos in phi]
        phi.sort(reverse=True)

        phi_tot.extend(iter(phi))
        return sum(phi_tot) / len(phi_tot)
    
    def set_behaviour1(self, b1 : behaviours) -> None:
        self.b1 = b1

    def set_behaviour2(self, b2 : behaviours) -> None:
        self.b2 = b2