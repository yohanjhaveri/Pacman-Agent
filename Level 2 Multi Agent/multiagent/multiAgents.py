# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#

"""
THIS CODE WAS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING ANY SOURCES OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR.
name: 'Yohan Jhaveri'
userID: 'yjhaver'
email: 'yohan.jhaveri@emory.edu'
"""

from util import manhattanDistance
from game import Directions
import random, util

import math

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
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currentFood = currentGameState.getFood() #food available from current state
        newFood = successorGameState.getFood() #food available from successor state (excludes food@successor)
        currentCapsules=currentGameState.getCapsules() #power pellets/capsules available from current state
        newCapsules=successorGameState.getCapsules() #capsules available from successor (excludes capsules@successor)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        food_closest = float('Inf')
        ghost_closest = float('Inf')

        food_list = newFood.asList()

        for food in food_list:
            food_distance = manhattanDistance(newPos, food)
            food_closest = min(food_closest, food_distance)

        for ghost in newGhostStates:
            ghost_distance = manhattanDistance(newPos, ghost.getPosition())
            ghost_closest = min(ghost_closest, ghost_distance)

        ghost_closest = ghost_closest or -float('Inf')
        food_closest = 0 if food_closest == float('Inf') else food_closest

        food_eaten = len(currentFood.asList()) - len(newFood.asList())

        return ghost_closest + 100 * food_eaten - 10 * food_closest


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
        """
        "*** YOUR CODE HERE ***"

        def get_scores(state, agent, depth):
            next_agent = (agent + 1) % state.getNumAgents()
            actions = state.getLegalActions(agent)
            return [minimax(state.generateSuccessor(agent, action), next_agent, depth + (next_agent == 0)) for action in actions]

        def minimax(state, agent, depth):
            if state.isLose() or state.isWin() or depth == self.depth:
                return self.evaluationFunction(state)

            if agent:   return min(get_scores(state, agent, depth))
            else:       return max(get_scores(state, agent, depth))

        actions = gameState.getLegalActions(0)
        return max([(minimax(gameState.generateSuccessor(0, action), 1, 0), action) for action in actions])[1]



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def maximizer(state, agent, depth, alpha, beta):
            score = -float('Inf')

            next_agent = (agent + 1) % state.getNumAgents()
            next_depth = depth + (next_agent == 0)

            actions = state.getLegalActions(agent)

            for action in actions:
                score = max(score, alpha_beta(state.generateSuccessor(agent, action), next_agent, next_depth, alpha, beta))
                alpha = max(alpha, score)
                if beta < score: break

            return score


        def minimizer(state, agent, depth, alpha, beta):
            score = float('Inf')

            next_agent = (agent + 1) % state.getNumAgents()
            next_depth = depth + (next_agent == 0)

            actions = state.getLegalActions(agent)

            for action in actions:
                score = min(score, alpha_beta(state.generateSuccessor(agent, action), next_agent, next_depth, alpha, beta))
                beta = min(beta, score)
                if score < alpha: break

            return score


        def game_over(state, depth):
            return state.isLose() or state.isWin() or depth == self.depth


        def alpha_beta(state, agent, depth, alpha, beta):
            if game_over(state, depth):
                return self.evaluationFunction(state)

            if agent:   return minimizer(state, agent, depth, alpha, beta)
            else:       return maximizer(state, agent, depth, alpha, beta)


        utility = -float('Inf')
        final_action = Directions.WEST

        alpha = -float('Inf')
        beta = float('Inf')

        actions = gameState.getLegalActions(0)

        for action in actions:

            ghost_utility = alpha_beta(gameState.generateSuccessor(0, action), 1, 0, alpha, beta)

            if ghost_utility > utility:
                utility = ghost_utility
                final_action = action

            if utility > beta: return utility

            alpha = max(alpha, utility)

        return final_action


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

        def expectimax(state, agent, depth):
            if agent < state.getNumAgents():

                actions = state.getLegalActions(agent)

                if actions:
                    next = [expectimax(state.generateSuccessor(agent, action), agent + 1, depth) for action in actions]

                    average = sum(next) / len(next)
                    maximum = max(next)

                    if agent:   return average
                    else:       return maximum

                else:
                    return self.evaluationFunction(state)

            else:
                if depth == self.depth: return self.evaluationFunction(state)
                else:                   return expectimax(state, 0, depth + 1)

        actions = gameState.getLegalActions(0)
        return max([(expectimax(gameState.generateSuccessor(0, action), 1, 1), action) for action in actions])[1]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newFoodList = newFood.asList()
    newCapsule = currentGameState.getCapsules()
    newGhostStates = currentGameState.getGhostStates()

    food_list = newFood.asList()

    food_closest = float('Inf')
    ghost_closest = float('Inf')

    for food in food_list:
        food_distance = manhattanDistance(newPos, food)
        food_closest = min(food_closest, food_distance)

    for ghost in newGhostStates:
        ghost_distance = manhattanDistance(newPos, ghost.getPosition())
        ghost_closest = min(ghost_closest, ghost_distance)

    numberOfCapsules = len(newCapsule)

    """Combination of the above calculated metrics."""
    return currentGameState.getScore() + (1 / float(food_closest or 1)) - (1 / float(ghost_distance or 1)) - numberOfCapsules

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
