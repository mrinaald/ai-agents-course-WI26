# valueIterationAgents.py
# -----------------------
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


import mdp, util
import pacman
from game import Agent, Actions


class PacmanMDP(mdp.MarkovDecisionProcess):
    """
    MDP for Pacman world.

    ================ WARNING ===============
    Don't make any change within this class.
    ========================================

    Note: The cartesian coordinate (x, y) of grid is:

        (0, 0) (0, 1) (0, 2) ...
        (1, 0) (1, 1)
        (2, 0)
        ...

    e.g., for the tinySimple layout (see the `layouts/tinySimple.lay` file),

        grid[0][0] <- '%'
        grid[1][1] <- 'G'
        grid[2][4] <- 'P'
        grid[6][6] <- '.'
    """

    def __init__(self, layout):
        self.layout = layout
        self.grid = layout.layoutText
        self.terminalState = 'TERMINAL_STATE'
        self.livingReward = 0.0
        self.noise = 0.0 # noise is not used in this assignment.

    def getStates(self):
        """
        Return a list of all states in the MDP.
        """
        states = []
        for y in range(self.layout.width):
            for x in range(self.layout.height):
                if self.grid[x][y] != '%':
                    state = (x, y)
                    states.append(state)
        return states

    def getStartState(self):
        """
        Return the start state of the MDP.
        Note: the start state does not matter in this assignment.
        """
        util.raiseNotDefined()

    def getPossibleActions(self, state):
        """
        Return list of possible actions from 'state'.
        """
        x, y = state
        if self.grid[x][y] in [".", "G"]:
            return ['Stop']

        possible = []
        for dir, (dx, dy) in Actions._directionsAsList:
            if self.grid[x + dx][y - dy] != "%":
                possible.append(dir)

        return possible

    def getTransitionStatesAndProbs(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.
        """

        if action not in self.getPossibleActions(state):
            raise Exception("Illegal action!")

        if self.isTerminal(state):
            return []

        x, y = state

        if self.grid[x][y] in [".", "G"]:
            termState = self.terminalState
            return [(termState, 1.0)]

        successors = []

        northState = (self.__isAllowed(x,y-1) and (x,y-1)) or state
        westState = (self.__isAllowed(x-1,y) and (x-1,y)) or state
        southState = (self.__isAllowed(x,y+1) and (x,y+1)) or state
        eastState = (self.__isAllowed(x+1,y) and (x+1,y)) or state

        if action == 'North':
            successors.append((northState, 1-self.noise))
        elif action == 'South':
            successors.append((southState, 1-self.noise))
        elif action == 'West' :
            successors.append((westState, 1-self.noise))
        elif action == 'East':
            successors.append((eastState, 1-self.noise))

        successors = self.__aggregate(successors)

        return successors

    def getReward(self, state, action, nextState):
        """
        Get the reward for the state, action, nextState transition.

        Not available in reinforcement learning.
        """
        x, y = state

        if self.grid[x][y] == ".": return 1
        elif self.grid[x][y] == "G": return -1

        return self.livingReward

    def isTerminal(self, state):
        """
        Returns true if the current state is a terminal state.  By convention,
        a terminal state has zero future rewards.  Sometimes the terminal state(s)
        may have no possible actions.  It is also common to think of the terminal
        state as having a self-loop action 'pass' with zero reward; the formulations
        are equivalent.
        """
        return state == self.terminalState

    def __aggregate(self, statesAndProbs):
        counter = util.Counter()
        for state, prob in statesAndProbs:
            counter[state] += prob
        newStatesAndProbs = []
        for state, prob in list(counter.items()):
            newStatesAndProbs.append((state, prob))
        return newStatesAndProbs

    def __isAllowed(self, x, y):
        if x < 0 or x >= self.layout.height: return False
        if y < 0 or y >= self.layout.width: return False
        return self.grid[x][y] != '%'


class ValueIterationAgent(Agent):
    """
        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) that is used to estimate Q-Values before
        actually acting.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        """
          Run the value iteration algorithm. Note that in standard
          value iteration, V_k+1(...) depends on V_k(...)'s.
        """
        "*** YOUR CODE HERE ***"

        # V_{k+1} (s) = max_a sum_{s'} T(s, a, s') [ R(s, a, s') + gamma * V_k(s') ]

        for _ in range(self.iterations):
            V_k = self.values.copy()

            for state in self.mdp.getStates():
                self.values[state] = 0

                Q_values = []
                for ai, action in enumerate(self.mdp.getPossibleActions(state)):
                    Q_value = 0

                    for next_state, transition_prob in self.mdp.getTransitionStatesAndProbs(state, action):
                        reward = self.mdp.getReward(state, action, next_state)
                        Q_value += transition_prob * (reward + (self.discount * V_k[next_state]))

                    Q_values.append(Q_value)

                if Q_values:
                    self.values[state] = max(Q_values)
                # else:
                #     self.values[state] = 0


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        Q_value = 0
        for next_state, transition_prob in self.mdp.getTransitionStatesAndProbs(state, action):
            reward = self.mdp.getReward(state, action, next_state)
            Q_value += transition_prob * (reward + (self.discount * self.values[next_state]))
        return Q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        Q_values = []
        possible_actions = self.mdp.getPossibleActions(state)
        for ai, action in enumerate(possible_actions):
            Q_value = 0
            for next_state, transition_prob in self.mdp.getTransitionStatesAndProbs(state, action):
                reward = self.mdp.getReward(state, action, next_state)
                Q_value += transition_prob * (reward + (self.discount * self.values[next_state]))
            Q_values.append(Q_value)

        if not Q_values:
            return None

        best_action_index = Q_values.index(max(Q_values))
        return possible_actions[best_action_index]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
