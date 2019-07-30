# multiAgents.py
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        metric = util.manhattanDistance
        score = 0 # = successorGameState.getScore()
        punishGhostLambdas = {0: -7000, 1: -1000, 2: -30, 3: -10, 4:-4, 5:-2}
        nearFoodBonusDict = {0: 30, 1: 20, 2: 12, 3:7, 4:4}
        foodRemPunishK = -20
        foodCount = newFood.count(True)
        if(foodCount ==0):
            return 9999
        nearFoodDist = 100
        for i, item in enumerate(newFood):
            for j, foodItem in enumerate(item):
                nearFoodDist = min(nearFoodDist, metric(newPos, (i, j)) if foodItem else 100)
        nearFoodBonus = nearFoodBonusDict[nearFoodDist] if nearFoodDist in nearFoodBonusDict else (3 + 1/nearFoodDist)
        foodRemPunish = foodRemPunishK*foodCount
        print foodCount, nearFoodDist
        ghostDistances = [metric(newPos, hh.getPosition()) for hh in newGhostStates]
        ghostK = sum([punishGhostLambdas[dist] for dist in ghostDistances if dist in punishGhostLambdas])

        score = score + nearFoodBonus + ghostK + foodRemPunish*foodCount
        print "score: ", score, ghostK
        return score
        # return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(state, depth):
            if depth == self.depth * state.getNumAgents() or state.isWin() or state.isLose():
                return None, self.evaluationFunction(state)
            agent = depth % state.getNumAgents()
            if agent == 0:
                return max_value(state, depth)
            return min_value(state, depth)

        def max_value(state, depth):
            agent = depth % state.getNumAgents()
            action, value = None, float("-inf")
            for a in state.getLegalActions(agent):
                _, v = minimax(state.generateSuccessor(agent, a), depth+1)
                action, value = max((a, v), (action, value), key=lambda x: x[1])
            return action, value

        def min_value(state, depth):
            agent = depth % state.getNumAgents()
            action, value = None, float("inf")
            for a in state.getLegalActions(agent):
                _, v = minimax(state.generateSuccessor(agent, a), depth+1)
                action, value = min((a, v), (action, value), key=lambda x: x[1])
            return action, value

        action, _ = minimax(gameState, self.index)
        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        from operator import gt, lt

        def alphabeta(state, depth, alpha, beta):
            if depth == self.depth * state.getNumAgents() or state.isLose() or state.isWin():
                return None, self.evaluationFunction(state)
            agent = depth % state.getNumAgents()
            OP = gt if agent == 0 else lt
            action, value = None, float('-inf') if agent == 0 else float('inf')
            for a in state.getLegalActions(agent):
                _, v = alphabeta(state.generateSuccessor(agent, a), depth+1, alpha, beta)
                action, value = (a, v) if OP(v, value) else (action, value)
                alpha = max(alpha, value) if agent == 0 else alpha  # Max
                beta = min(beta, value) if agent != 0 else beta     # Min
                if alpha > beta:
                    break
            return action, value

        action, _ = alphabeta(gameState, self.index, float('-inf'), float('inf'))
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        from operator import itemgetter
        ACTION, VALUE = itemgetter(0), itemgetter(1)

        def expectimax(state, depth):
            if depth == self.depth * state.getNumAgents() or state.isLose() or state.isWin():
                return None, self.evaluationFunction(state)
            agent = depth % state.getNumAgents()
            OP = max if agent == 0 else lambda lst, key: (None, sum(key(i) for i in lst)/float(len(lst)))
            return OP([(action, VALUE(expectimax(state.generateSuccessor(agent, action), depth+1)))for action in state.getLegalActions(agent)], key=VALUE)

        return ACTION(expectimax(gameState, self.index))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    return currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction

