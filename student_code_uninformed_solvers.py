
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.explored=[]

    
    def findAcceptableState(self):
        if not isinstance(self.currentState,GameState):
            raise Exception("Error 1")
        acceptable = self.currentState.nextChildToVisit<len(self.currentState.children)
        while not acceptable:
            self.currentState = self.currentState.parent
            acceptable = self.currentState.nextChildToVisit<len(self.currentState.children)
            if not isinstance(self.currentState,GameState):
                raise Exception("Error 2")
        self.currentState.nextChildToVisit+=1
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
        self.explored.append(self.currentState.state)
        
        #Step 2
        moveoptions=self.gm.getMovables()
        for option in moveoptions:
            self.gm.makeMove(option)
            newchild = GameState(self.gm.getGameState,self.currentState.depth+1,option)
            newchild.parent=self.currentState
            if self.currentState.state not in self.explored:
                self.currentState.children.append(newchild)
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
        self.nextDepth=[]
        self.currentDepth=[]
        self.index=0
        self.depthindex=0
        self.explored=[]
        
    def findAcceptableState(self):
        if self.index<len(self.currentDepth):
            self.currentState=self.currentDepth[self.index]
            self.index+=1
            return True
        
        self.currentDepth=self.nextDepth
        #if self.nextDepth==[]:
            #breakpoint()
        self.nextDepth=[]
        self.currentState=self.currentDepth[0]
        self.index=1
        return True
    
    def findAcceptableStateMeme(self):
        while self.index<len(self.currentDepth):
            if self.currentDepth[self.index].depth==self.depthindex:
                break
        if self.currentDepth[self.index].depth==self.depthindex:
            self.currentState=self.currentDepth[self.index]
            self.index+=1
            return
        self.depthindex+=1
        self.index=0
        findAcceptableStateMeme()
        return
        
    def solveOneStep(self):
        ###Note to self: Plan is to use the children as something to work with, change current states as the main way we do things
        ### Student code goes here
         #Step 1
        if self.currentState.state==self.victoryCondition:
            return True
        self.explored.append(self.currentState.state)
        #Step 2
        moveoptions=self.gm.getMovables()
        for option in moveoptions:
            self.gm.makeMove(option)
            newchild = GameState(self.gm.getGameState,self.currentState.depth+1,option)
            self.currentDepth.append(newchild)
            self.gm.reverseMove(option)
            
        #Step 3

        self.findAcceptableStateMeme()
        return False
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
"""
        ###Note to self: Plan is to use the children as something to work with, change current states as the main way we do things
        ### Student code goes here
         #Step 1
        if self.gm.getGameState()==self.victoryCondition:
            return True
        self.explored.append(self.currentState.state)
        #Step 2
        moveoptions=self.gm.getMovables()
        for option in moveoptions:
            self.gm.makeMove(option)
            newchild = GameState(self.gm.getGameState,self.currentState.depth+1,option)
            newchild.parent=self.currentState
            self.currentState.children.append(newchild)
            if newchild.state not in self.explored:
                self.nextDepth.append(newchild)
            self.gm.reverseMove(option)
            
        #Step 3
        
        self.findAcceptableState()
        return False"""

