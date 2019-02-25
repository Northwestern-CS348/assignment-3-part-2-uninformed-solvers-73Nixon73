
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.explored=[]

    
    def findAcceptableState(self):
        acceptable = self.currentState.nextChildToVisit<len(self.currentState.children)
        while not acceptable:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            acceptable = self.currentState.nextChildToVisit<len(self.currentState.children)
        self.currentState.nextChildToVisit+=1
        self.gm.makeMove(self.currentState.children[self.currentState.nextChildToVisit-1].requiredMovable)
        self.currentState=self.currentState.children[self.currentState.nextChildToVisit-1]
        return
    """
        if self.currentState.nextChildToVisit<len(self.currentState.children):
            self.currentState.nextChildToVisit+=1
            self.currentState=self.currentState.children[self.currentState.nextChildToVisit-1]
            return True
        self.currentState=self.currentState.parent
        return False
"""
    def solveOneStep(self):

        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here 1. Victory Condition 2. Children 3. Search parameter
        ### Student code goes here
        #Step 1
        if self.currentState.state==self.victoryCondition:
            return True
        
        
        #Step 2
        moveoptions=self.gm.getMovables()
        for option in moveoptions:
            self.gm.makeMove(option)
            newchild = GameState(self.gm.getGameState(),self.currentState.depth+1,option)
            newchild.parent=self.currentState
            if newchild.state not in self.explored:
                self.currentState.children.append(newchild)
                self.explored.append(newchild.state)
            self.gm.reverseMove(option)
            
        #Step 3
        """
        if self.currentState in self.visited:
            if isinstance(self.currentState.parent,GameState):
                
                notusable = self.currentState.parent.nextChildToVisit>=len(self.currentState.parent.children)
                
                while notusable:
                    self.currentState=self.currentState.parent
                    notusable = isinstance(self.currentState.parent, GameState)
                    if notusable:
                        notusable=self.currentState.parent.nextChildToVisit>=len(self.currentState.parent.children)
            
            
                self.currentState.nextChildToVisit+=1
                self.currentState=self.currentState.children[self.currentState.nextChildToVisit-1]
                return False
        """
        self.findAcceptableState()
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.explored=[]
        self.depthindex=0

    def findNextUnexploredPath(self):
        if not isinstance(self.currentState.parent,GameState):
            return False
        self.gm.reverseMove(self.currentState.requiredMovable)
        self.currentState=self.currentState.parent
        while self.currentState.nextChildToVisit>=len(self.currentState.children):
            if not isinstance(self.currentState.parent,GameState):
                if len(self.currentState.children)>self.currentState.nextChildToVisit:
                    return True
                return False
            #Go back 1
            #When leave one behind,mark next child as 0. Only do so to things left behind.
            self.currentState.nextChildToVisit=0
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState=self.currentState.parent 
            

        return True
    
    def findNewDepth(self):
        while not self.explorePath():
            if not self.findNextUnexploredPath():
                self.depthindex+=1  
        return            

    def explorePath(self):
        while self.currentState.depth<self.depthindex and len(self.currentState.children)>self.currentState.nextChildToVisit:
            self.gm.makeMove(self.currentState.children[self.currentState.nextChildToVisit].requiredMovable)
            self.currentState.nextChildToVisit+=1
            self.currentState=self.currentState.children[self.currentState.nextChildToVisit-1]
        if self.currentState.depth!=self.depthindex:
            return False
        return True
    
    def findAcceptableState(self):
        if (not isinstance(self.currentState.parent,GameState)):
            self.depthindex+=1
            self.findNewDepth()
            return
        #Sibling Case
        if self.currentState.parent.nextChildToVisit<len(self.currentState.parent.children):
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState=self.currentState.parent
            self.gm.makeMove(self.currentState.children[self.currentState.nextChildToVisit].requiredMovable)
            self.currentState.nextChildToVisit+=1
            self.currentState=self.currentState.children[self.currentState.nextChildToVisit-1]
            return
        
        while self.findNextUnexploredPath():
            if self.explorePath():
                return
            
        ##New Depth Case
        if (not isinstance(self.currentState.parent,GameState)) and self.currentState.nextChildToVisit>=len(self.currentState.children):
            self.currentState.nextChildToVisit=0
            self.depthindex+=1
            self.findNewDepth()
        return

    def solveOneStep(self):
        ###Note to self: Plan is to use the children as something to work with, change current states as the main way we do things

       #Step 1
        if self.currentState.state==self.victoryCondition:
            return True
        
        
        #Step 2
        moveoptions=self.gm.getMovables()
        for option in moveoptions:
            self.gm.makeMove(option)
            newchild = GameState(self.gm.getGameState(),self.currentState.depth+1,option)
            newchild.parent=self.currentState
            if newchild.state not in self.explored:
                self.currentState.children.append(newchild)
                self.explored.append(newchild.state)
            self.gm.reverseMove(option)
        
        #Step 3
        self.findAcceptableState()
        return False

