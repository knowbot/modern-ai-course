# pacmanAgents.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from pacman import Directions
from game import Agent
import copy
import random
import game
import util
from enum import Enum

class BaseAgent(game.Agent):
    class State:
        def __init__(self):
            self.actions = ['GoRight','GoLeft','GoForward','GoBack']

    def registerInitialState(self, state):
        """AgentState is stored in state"""
        self._dir = 0
        self._dirsMap = {(1,0):'East',(0,-1):'South',(-1,0):'West',(0,1):'North'}
        self._dirs = [(1,0),(0,-1),(-1,0),(0,1)]
        self._percept = ('clear', None)
        self._actions = ['GoRight','GoLeft','GoForward','GoBack']
        self._state = self.State()
        
    def getAction(self, state):
        """Get the next action. Note that the state passed here is used only
        to identify legal actions."""
        self._state = self.update_state_with_percept(self._percept, self._state)
        action = self.choose_action(copy.deepcopy(self._state))
        self._state = self.update_state_with_action(action, self._state)

        # Map the action
        do = self.mapAction(action)
        # If bump
        if do not in state.getLegalPacmanActions() and do != "Nothing":
            self._percept = ('clear','bump')
        else:
            self._percept = ('clear',None)
        
        return do
        
    def mapAction(self, action):
        """Map vacuum action to pacman action"""
        if action == "GoRight": self._dir += 1
        elif action == "GoLeft": self._dir -= 1
        elif action == "GoBack": self._dir += 2
        elif action == "GoForward": pass
        elif action == "Stop": return 'Stop'
        else: return "Nothing"
        self._dir %= 4
        
        return self._dirsMap[self._dirs[self._dir]]

    def update_state_with_percept(self, percept, state):
        """Update the agents state based on a percept"""
        return state

    def choose_action(self, state): 
        """Choose an action: GoLeft, GoRight, GoForward, GoBack, Stop"""
        return random.choice(self._actions)

    def update_state_with_action(self, action, state):
        """Update 'state' based on previous action"""
        return state

#from pacman import *
#args = readCommand(["--pacman","BaseAgent",#"PacmanWithState",
#                    "--layout","mediumEmpty"])
#runGames(**args)

class ZeroIntelligent(BaseAgent):
    class State:
        def __init__(self):
            self.actions = ["GoRight", "GoLeft", "GoForward", "GoBack"]

    def __init__(self, debug=False):
        self.debug = debug

    def choose_action(self, state):
        action = random.choice(state.actions)
        if self.debug:
            print("Performing action:", action)
        return action

class Intelligent(BaseAgent):
    class State:
        def __init__(self):
            self.bump = False
            self.previous_action = ""
            self.actions = ["GoRight", "GoLeft", "GoForward", "GoBack"]

        def __repr__(self):
            if self.bump:
                return self.previous_action + " resulted in a bump"
            else:
                return self.previous_action
    
    def __init__(self, debug=False):
        self.debug = debug
        
    def update_state_with_percept(self, percept, state):
        if percept[1] == "bump":
            state.bump = True
        else:
            state.bump = False
        return state

    def choose_action(self, state):
        actions = state.actions
        if state.bump:
            actions.remove(state.previous_action)
        return random.choice(actions)

    def update_state_with_action(self, action, state):
        state.previous_action = action
        # Print the representation (i.e. __repr__) of the state
        if self.debug:
            print(state)
        return state

class BehaviourTree(BaseAgent):
    class State:
        def __init__(self):
            self.actions = ["GoRight", "GoLeft", "GoForward", "GoBack"]
    
    class Node:
        Status = Enum('Status', 'INACTIVE SUCCESS RUNNING FAILURE')
        def __init__(self):
            self.status = Status.INACTIVE
            self.parent = None
            self.children = []
            
        def add_child(childNode):
            if childNode.parent == self:
                raise Exception('Nodes cannot be their own fathers :D')
            childNode.parent = self
            self.children.append(childNode)
            
        def tick():
            util.raiseNotDefined()
            
    class Sequence(Node):
        def __init__(self):
            super(Sequence, self).__init__()
            
        def tick():
            for child in self.children:
                child_status = child.tick()
                if child_status == Status.RUNNING:
                    return Status.RUNNING
                elif child_status == Status.FAILURE:
                    return Status.FAILURE
            return Status.SUCCESS
    
    class Fallback(Node):
        def __init__(self):
            super(Fallback, self).__init__()
            
        def tick():
            for child in self.children:
                child_status = child.tick()
                if child_status == Status.RUNNING:
                    return Status.RUNNING
                elif child_status == Status.SUCCESS:
                    return Status.SUCCESS
            return Status.FAILURE
            
        
    class Parallel(Node):
        def __init__(self):
            super(Parallel, self).__init__()
            
        def tick():
            child_statuses = []
            for child in self.children:
                child_statuses.append(child.tick())
            if Status.SUCCESS in child_statuses:
                return Status.SUCCESS
            elif Status.RUNNING not in child_statuses:
                return Status.FAILURE
            return Status.RUNNING
              
        