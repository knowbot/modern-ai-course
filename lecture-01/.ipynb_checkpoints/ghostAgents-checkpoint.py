# ghostAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util
from numpy import random

class GhostAgent( Agent ):
    def __init__( self, index ):
        self.index = index

    def getAction( self, state ):
        distribution = self.getDistribution(state)
        if len(distribution) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(distribution)

    def getDistribution(self, state):
        util.raiseNotDefined()

class RandomGhost( GhostAgent ):
    def getDistribution( self, state ):
        distribution = util.Counter()
        # all actions have the same chance of happening
        for action in state.getLegalActions(self.index): distribution[action] = 1.0
        # normalize distribution and pick at random
        distribution.normalize()
        return distribution
