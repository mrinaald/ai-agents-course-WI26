# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    dfs = util.Stack()
    action_path = {}

    dfs.push((None, None, start))

    goal_state = None
    while not dfs.isEmpty():
        prev_state, action, state = dfs.pop()

        if state in action_path:
            continue

        action_path[state] = (prev_state, action)

        if problem.isGoalState(state):
            goal_state = state
            break

        successors = problem.getSuccessors(state)
        # print(f"State: {state} | Successors: {successors}")
        for next_state, action, cost in successors:
            if next_state not in action_path:
                dfs.push((state, action, next_state))

    # print(f"Goal state: {state} | {problem.isGoalState(state)}")
    action_seq = []
    state = goal_state
    while True:
        state, action = action_path[state]
        if action is None:
            break
        action_seq.append(action)

    # print(f"Action sequence: {action_seq[::-1]}")
    return action_seq[::-1]

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    bfs = util.Queue()
    action_path = {}

    bfs.push((None, None, start, 0))

    goal_state = None
    while not bfs.isEmpty():
        prev_state, action, state, cost = bfs.pop()

        if state in action_path and cost >= action_path[state][2]:
            continue

        action_path[state] = (prev_state, action, cost)

        if problem.isGoalState(state):
            goal_state = state
            break

        successors = problem.getSuccessors(state)
        for next_state, action, c in successors:
            if next_state in action_path and cost + c >= action_path[next_state][2]:
                continue

            bfs.push((state, action, next_state, cost + c))

    # print(f"Goal state: {state} | {problem.isGoalState(state)}")
    action_seq = []
    state = goal_state
    while True:
        state, action, _ = action_path[state]
        if action is None:
            break
        action_seq.append(action)

    # print(f"Action sequence: {action_seq[::-1]}")
    return action_seq[::-1]

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    pq = util.PriorityQueue()
    action_path = {}

    pq.push((None, None, start, 0), 0)

    goal_state = None
    while not pq.isEmpty():
        prev_state, action, state, cost = pq.pop()
        if state in action_path and cost >= action_path[state][2]:
            continue

        action_path[state] = (prev_state, action, cost)

        if problem.isGoalState(state):
            goal_state = state
            break

        successors = problem.getSuccessors(state)
        for next_state, action, c in successors:
            if next_state in action_path and cost + c >= action_path[next_state][2]:
                continue

            pq.push((state, action, next_state, cost + c), cost + c)

    # print(f"Goal state: {state} | {problem.isGoalState(state)}")
    action_seq = []
    state = goal_state
    while True:
        state, action, _ = action_path[state]
        if action is None:
            break
        action_seq.append(action)

    # print(f"Action sequence: {action_seq[::-1]}")
    return action_seq[::-1]

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    pq = util.PriorityQueue()
    action_path = {}

    pq.push((None, None, start, 0), 0 + heuristic(start, problem))

    goal_state = None
    while not pq.isEmpty():
        prev_state, action, state, cost = pq.pop()
        if state in action_path and cost >= action_path[state][2]:
            continue

        action_path[state] = (prev_state, action, cost)

        if problem.isGoalState(state):
            goal_state = state
            break

        successors = problem.getSuccessors(state)
        for next_state, action, c in successors:
            if next_state in action_path and cost + c >= action_path[next_state][2]:
                continue

            pq.push((state, action, next_state, cost + c), cost + c + heuristic(next_state, problem))

    # print(f"Goal state: {state} | {problem.isGoalState(state)}")
    action_seq = []
    state = goal_state
    while True:
        state, action, _ = action_path[state]
        if action is None:
            break
        action_seq.append(action)

    # print(f"Action sequence: {action_seq[::-1]}")
    return action_seq[::-1]

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
