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
        closesthost=float("Inf")
        for state in newGhostStates:
          closesthost=min(manhattanDistance(state.getPosition(),newPos),closesthost)
        
        numFood = successorGameState.getNumFood()
        prevNumFood = currentGameState.getNumFood()
        if closesthost<=1:
          return float("-Inf")
        
        
        currentFood=newFood.asList()
        minFoodDis=0
        FoodDis=[]
        for food in currentFood:
          FoodDis.append( manhattanDistance(food,newPos))
        if len(FoodDis)>0:
          minFoodDis=min(FoodDis)
        return  successorGameState.getScore() - minFoodDis + 100*(prevNumFood - numFood)

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
    def minimax(self,gameState,depth,agentIndex):
          if depth==self.depth or gameState.isWin() or gameState.isLose():
            return gameState.getScore()
          if agentIndex==0:
            pacman=True
          else:
            pacman=False
           
          if pacman:
            bestScore=float("-Inf")
            for action in gameState.getLegalActions(agentIndex):
                state=gameState.generateSuccessor(agentIndex,action)
                score=self.minimax(state,depth,agentIndex+1)
                bestScore=max(score,bestScore)
            return bestScore
          else:

            bestScore=float("Inf")
            for action in gameState.getLegalActions(agentIndex):
                state=gameState.generateSuccessor(agentIndex,action)
                
                if agentIndex==gameState.getNumAgents()-1:
                  score=self.minimax(state,depth+1,0)
                else:
                  score=self.minimax(state,depth,agentIndex+1)
                bestScore=min(score,bestScore)
            
            return bestScore
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
        legal = gameState.getLegalActions(0)
        ans_act = None 
        mxv = -999999
        for act in legal :
            succ_state = gameState.generateSuccessor(0 ,act)
            v= self.minimax(succ_state , 0 , 1)
            if v>= mxv :
                mxv =v
                ans_act = act        
        #print (ans_act)
        return ans_act
        
     


        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def AlphaMetaMinimax(self,gameState,depth,agentIndex,alpha=-99999999,beta=99999999):
          if depth==self.depth or gameState.isWin() or gameState.isLose():
            return gameState.getScore()
          if agentIndex==0:
            pacman=True
          else:
            pacman=False
           
          if pacman:
            bestScore=float("-Inf")
            for action in gameState.getLegalActions(agentIndex):
                state=gameState.generateSuccessor(agentIndex,action)
                score=self.AlphaMetaMinimax(state,depth,agentIndex+1,alpha,beta)
                bestScore=max(score,bestScore)
                if bestScore>beta:
                  return bestScore
                alpha=max(alpha,bestScore)
            return bestScore
          else:

            bestScore=float("Inf")
            for action in gameState.getLegalActions(agentIndex):
                state=gameState.generateSuccessor(agentIndex,action)
                
                if agentIndex==gameState.getNumAgents()-1:
                  score=self.AlphaMetaMinimax(state,depth+1,0,alpha,beta)
                else:
                  score=self.AlphaMetaMinimax(state,depth,agentIndex+1,alpha,beta)
                bestScore=min(score,bestScore)
                if bestScore < alpha:
                  return bestScore
                beta=min(beta,bestScore)
            
            return bestScore
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        legal = gameState.getLegalActions(0)
        ans_act = None 
        mxv = -999999
        alphaRoot=-999999
        for act in legal :
            succ_state = gameState.generateSuccessor(0 ,act)
            v= self.AlphaMetaMinimax(succ_state , 0 , 1,alpha=alphaRoot)
            if v>= mxv :
                mxv =v
                ans_act = act
                alphaRoot=v        
        #print (ans_act)
        return ans_act
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimax(self,gameState,depth,agentIndex):
          if depth==self.depth or gameState.isWin() or gameState.isLose():
            return gameState.getScore()
          if agentIndex==0:
            pacman=True
          else:
            pacman=False
           
          if pacman:
            bestScore=float("-Inf")
            for action in gameState.getLegalActions(agentIndex):
                state=gameState.generateSuccessor(agentIndex,action)
                score=self.expectimax(state,depth,agentIndex+1)
                bestScore=max(score,bestScore)
            return bestScore
          else:

            bestScore=0
            acts=gameState.getLegalActions(agentIndex)
            for action in acts:
                state=gameState.generateSuccessor(agentIndex,action)
                
                if agentIndex==gameState.getNumAgents()-1:
                  score=self.expectimax(state,depth+1,0)
                else:
                  score=self.expectimax(state,depth,agentIndex+1)
                bestScore+=score
            
            return bestScore/len(acts)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        legal = gameState.getLegalActions(0)
        ans_act = None 
        mxv = -999999
        for act in legal :
            succ_state = gameState.generateSuccessor(0 ,act)
            v= self.expectimax(succ_state , 0 , 1)
            if v>= mxv :
                mxv =v
                ans_act = act        
        #print (ans_act)
        return ans_act
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


    foodDistances = []
    mdscore = 0
    ghostPositions = [manhattanDistance(newPos, i.getPosition()) for i in newGhostStates]
    mdgav = reduce(lambda x, y: x+y, ghostPositions)/len(ghostPositions)

    if not newFood.asList():
        mdscore = 0
    else:
        foodDistances = [manhattanDistance(newPos,i) for i in newFood.asList()]
        mdscore = min(foodDistances)

    return currentGameState.getScore() + min(newScaredTimes) + 1/(mdscore + 0.1) - (1/(mdgav + 0.11))
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction