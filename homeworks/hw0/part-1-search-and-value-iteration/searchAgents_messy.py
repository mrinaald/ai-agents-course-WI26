# searchAgents.py
# ---------------
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
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the project
description.

Please only change the parts of the file you are asked to.  Look for the lines
that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the project
description for details.

Good luck and happy searching!
"""

from typing import List, Tuple, Any
from game import Directions
from game import Agent
from game import Actions
import util
import time
import search
import pacman

class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state) # Makes a new search problem
        self.actions  = self.searchFunction(problem) # Find a path
        if self.actions == None:
            self.actions = []
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn, (1, 1), None, False)

class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState: pacman.GameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost


class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem


# mrinaal = 0
def foodHeuristic(state: Tuple[Tuple, List[List]], problem: FoodSearchProblem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your search may have a but our your heuristic is not admissible!  On the
    other hand, inadmissible heuristics may find optimal solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state
    "*** YOUR CODE HERE ***"
    # global mrinaal
    # mrinaal += 1
    # if mrinaal == 1:
    #     print(problem.getStartState())
    #     print(position)
    #     print(foodGrid)
    #     print(foodGrid.asList())
    #     print(problem.walls)
    #     print(problem.walls.count())
    #     print(problem.walls.asList())

    # ################################
    # # Priority queue based
    # # Verdict: Too slow, and too much exploration
    # ################################
    # food_cells = foodGrid.asList()
    # if len(food_cells) == 0:
    #     # goal state
    #     return 0

    # pq = util.PriorityQueue()
    # dist = {}
    # cost_to_reach_food = {}
    # num_food_found = 0
    # total_food = len(food_cells)

    # pq.push((state, 0), 0)
    # dist[position] = 0

    # while pq and num_food_found < total_food:
    #     state, curr_cost = pq.pop()
    #     pos = state[0]
    #     if foodGrid[pos[0]][pos[1]]:
    #         if pos not in cost_to_reach_food:
    #             num_food_found += 1
    #             cost_to_reach_food[pos] = curr_cost
    #         else:
    #             cost_to_reach_food[pos] = min(cost_to_reach_food[pos], curr_cost)

    #     successors = problem.getSuccessors(state)
    #     for next_state, _, c in successors:
    #         next_pos = next_state[0]
    #         if next_pos in dist and curr_cost + c >= dist[next_pos]:
    #             continue

    #         dist[next_pos] = curr_cost + c
    #         pq.push((next_state, curr_cost + c), curr_cost + c)

    # return min(cost_to_reach_food.values())

    # ################################
    # # Simple manhatten distance based approach
    # # Verdict: with min(), explored < 15000 nodes
    # #          with average(), explored < 12000 nodes
    # ################################
    # food_cells = foodGrid.asList()
    # if len(food_cells) == 0:
    #     # goal state
    #     return 0

    # manhattan_distances = [util.manhattanDistance(position, food_pos) for food_pos in food_cells]

    # # return min(manhattan_distances)

    # return sum(manhattan_distances) / len(manhattan_distances)

    # # manhattan_distances.sort()
    # # l = len(manhattan_distances)
    # # if l % 2 == 1:
    # #     return manhattan_distances[l // 2]
    # # else:
    # #     return (manhattan_distances[l // 2 - 1] + manhattan_distances[l // 2]) / 2

    ################################
    # Food Distance dp
    ################################
    food_cells = foodGrid.asList()
    if len(food_cells) == 0:
        # goal state
        problem.heuristicInfo.pop("dp", None)
        problem.heuristicInfo.pop("food_cells", None)
        return 0

    def do_bfs(start, dp, walls, width, height, is_negative_bfs: bool = False):
        is_visited = [[False] * height for _ in range(width)]

        bfs = util.Queue()
        bfs.push(start)
        is_visited[start[0]][start[1]] = True
        steps = 0
        while not bfs.isEmpty():
            level_size = len(bfs.list)
            for _ in range(level_size):
                cell = bfs.pop()
                for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
                    dx, dy = Actions.directionToVector(direction)
                    nextx, nexty = cell[0] + int(dx), cell[1] + int(dy)
                    if 0 <= nextx < width and 0 <= nexty < height and not walls[nextx][nexty] and not is_visited[nextx][nexty]:
                        bfs.push((nextx, nexty))
                        is_visited[nextx][nexty] = True
                        if is_negative_bfs:
                            dp[nextx][nexty] -= (steps + 1)
                        else:
                            dp[nextx][nexty] += steps + 1
            steps += 1

    def get_steps(start, end, walls, width, height):
        is_visited = [[False] * height for _ in range(width)]

        bfs = util.Queue()
        bfs.push(start)
        is_visited[start[0]][start[1]] = True
        steps = 0
        while not bfs.isEmpty():
            level_size = len(bfs.list)
            for _ in range(level_size):
                cell = bfs.pop()
                if cell == end:
                    return steps
                for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
                    dx, dy = Actions.directionToVector(direction)
                    nextx, nexty = cell[0] + int(dx), cell[1] + int(dy)
                    if 0 <= nextx < width and 0 <= nexty < height and not walls[nextx][nexty] and not is_visited[nextx][nexty]:
                        bfs.push((nextx, nexty))
                        is_visited[nextx][nexty] = True
            steps += 1
        return float('inf')

    if "dp" not in problem.heuristicInfo:
        # calculate food distance dp
        problem.heuristicInfo["dp"] = {}

    dp = problem.heuristicInfo["dp"]

    for cell in food_cells:
        if cell in dp:
            continue
        cell_dp = [[0 for _ in range(foodGrid.height)] for _ in range(foodGrid.width)]
        do_bfs(cell, cell_dp, problem.walls, foodGrid.width, foodGrid.height)
        dp[cell] = cell_dp

    # if "food_cells" not in problem.heuristicInfo:
    #     # add all food cells in heuristicInfo
    #     problem.heuristicInfo["food_cells"] = set(food_cells)

    # removed_food_cells = list(problem.heuristicInfo["food_cells"] - set(food_cells))
    # num_steps = 0
    # for cell in removed_food_cells:
    #     num_steps += get_steps(cell, position, problem.walls, foodGrid.width, foodGrid.height)

    # if len(food_cells) != len(problem.heuristicInfo["food_cells"]):
    #     # some food has been eaten, reset dp
    #     # TODO: identify which food cell got removed
    #     print(problem.heuristicInfo["food_cells"])
    #     print(set(food_cells))
    #     print(problem.heuristicInfo["food_cells"] - set(food_cells))
    #     print()
    #     removed_food_cell = list(problem.heuristicInfo["food_cells"] - set(food_cells))[0]

    #     # TODO: reset dp
    #     do_bfs(removed_food_cell, dp, problem.walls, foodGrid.width, foodGrid.height, is_negative_bfs=True)

    #     problem.heuristicInfo["food_cells"].remove(removed_food_cell)

    h = 0
    for cell in food_cells:
        # h += dp[cell][position[0]][position[1]]
        h += (dp[cell][position[0]][position[1]] / util.manhattanDistance(position, cell))

    # Factor of 0.8 found using hit and trial
    return h * 0.8



def mazeDistance(point1: Tuple[int, int], point2: Tuple[int, int], gameState: pacman.GameState) -> int:
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))
