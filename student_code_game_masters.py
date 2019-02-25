from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        peglist=[[],[],[]]
        ##breakpoint()
        for x in range(1,4):
            for y in range(1,6):
                
                assertstr="fact: (on disk"+str(y)+" peg"+str(x)+")"
                asserty=self.kb.kb_ask(parse_input(assertstr))
                if asserty!=False:
                    peglist[x-1].append(y)
        peg1tuple=tuple(peglist[0])
        peg2tuple=tuple(peglist[1])
        peg3tuple=tuple(peglist[2])
        finallist=(peg1tuple,peg2tuple,peg3tuple)
        return finallist
        

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ###taking the terms
        disklist = ["disk1","disk2","disk3","disk4","disk5"]
        
        termlist=movable_statement.terms
        movedisk=termlist[0].term.element
        startpeg=termlist[1].term.element
        endpeg=termlist[2].term.element

        ###fact construction
        factpeg="fact: ("

        ##Note to self: Biggest problem so far is how to search for a fact to retract (i.e. taking off the peg's current top)
        ##Also how do I make facts in a less awful way.
        ### If destination is empty
        emptygoal = factpeg+"empty "+endpeg+")"
        emptygoalparsed = parse_input(emptygoal)
        emptygoaltest = self.kb.kb_ask(emptygoalparsed)
        
        if emptygoaltest==False:
            #retract the target being empty, the current peg being on top, and the current peg having the disk
            disklocation=factpeg+"on "+movedisk+" "+startpeg+")"
            self.kb.kb_retract(parse_input(disklocation))
            disklocation=factpeg+"top "+movedisk+" "+startpeg+")"
            self.kb.kb_retract(parse_input(disklocation))
            self.kb.kb_retract(emptygoalparsed)
            #assert the disk being on the new peg, it being on the new peg, and a new top for the starting peg
            self.kb.kb_assert(parse_input(factpeg+"on "+movedisk+" "+endpeg+")"))
            self.kb.kb_assert(parse_input(factpeg+"top "+movedisk+" "+endpeg+")"))
            changed=False
            for disk in disklist:
                ask=self.kb.kb_ask(parse_input(factpeg+"on "+disk+" "+startpeg+")"))
                if ask!=False & changed==False:
                    self.kb.kb_assert(parse_input(factpeg+"top "+disk+" "+startpeg+")"))
                    changed=True
            if changed==False:
                self.kb.kb_assert(parse_input(factpeg+"empty "+startpeg+")"))

        else:
            #retract the starting peg having the disk, it being on top, and the receiving peg having another top
            disklocation=factpeg+"on "+movedisk+" "+startpeg+")"
            self.kb.kb_retract(parse_input(disklocation))
            disklocation=factpeg+"top "+movedisk+" "+startpeg+")"
            self.kb.kb_retract(parse_input(disklocation))
            changed=False
            for disk in disklist:
                ask=self.kb.kb_ask(parse_input(factpeg+"top "+disk+" "+endpeg+")"))
                if ask!=False & changed==False:
                    self.kb.kb_retract(parse_input(factpeg+"top "+disk+" "+endpeg+")"))
                    changed=True

            #assert the starting peg having a new top, the new disk being on top of the new peg, and the disk being on the new peg
            self.kb.kb_assert(parse_input(factpeg+"on "+movedisk+" "+endpeg+")"))
            self.kb.kb_assert(parse_input(factpeg+"top "+movedisk+" "+endpeg+")"))
            changed=False
            for disk in disklist:
                ask=self.kb.kb_ask(parse_input(factpeg+"on "+disk+" "+startpeg+")"))
                if ask!=False & changed==False:
                    self.kb.kb_assert(parse_input(factpeg+"top "+disk+" "+startpeg+")"))
                    changed=True
            if changed==False:
                self.kb.kb_assert(parse_input(factpeg+"empty "+startpeg+")"))
        return
            
            


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        protuple=[[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]
        for tilenum in range(1,9):
            tile="tile"+str(tilenum)
            if self.kb.kb_ask(parse_input("fact: (coordinate "+tile+" pos1 pos1)"))!=False:
                protuple[0][0]=tilenum
            if self.kb.kb_ask(parse_input("fact: (coordinate "+tile+" pos2 pos1)"))!=False:
                protuple[1][0]=tilenum
            if self.kb.kb_ask(parse_input("fact: (coordinate "+tile+" pos3 pos1)"))!=False:
                protuple[2][0]=tilenum
            if self.kb.kb_ask(parse_input("fact: (coordinate "+tile+" pos1 pos2)"))!=False:
                protuple[0][1]=tilenum
            if self.kb.kb_ask(parse_input("fact: (coordinate "+tile+" pos2 pos2)"))!=False:
                protuple[1][1]=tilenum
            if self.kb.kb_ask(parse_input("fact: (coordinate "+tile+" pos3 pos2)"))!=False:
                protuple[2][1]=tilenum
            if self.kb.kb_ask(parse_input("fact: (coordinate "+tile+" pos1 pos3)"))!=False:
                protuple[0][2]=tilenum
            if self.kb.kb_ask(parse_input("fact: (coordinate "+tile+" pos2 pos3)"))!=False:
                protuple[1][2]=tilenum
            if self.kb.kb_ask(parse_input("fact: (coordinate "+tile+" pos3 pos3)"))!=False:
                protuple[2][2]=tilenum
        """
        for x in range (1,4):
            if self.kb.kb_ask(parse_input("fact: (ypos empty pos"+str(x)+")"))!=False:
                for y in range (1,4):
                    if self.kb.kb_ask(parse_input("fact: (xpos empty pos"+str(y)+")"))!=False:
                        protuple[x][y]=-1
                        """
        truetuple1=tuple(protuple[0])
        truetuple2=tuple(protuple[1])
        truetuple3=tuple(protuple[2])
        return (truetuple1, truetuple2, truetuple3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        #extract terms
        termlist=movable_statement.terms
        tile=termlist[0].term.element
        startposx=termlist[1].term.element
        startposy=termlist[2].term.element
        endposx=termlist[3].term.element
        endposy=termlist[4].term.element
        #breakpoint()
        #retract old facts
        self.kb.kb_retract(parse_input("fact: (xpos "+tile+" "+startposx+")"))
        #breakpoint()
        self.kb.kb_retract(parse_input("fact: (ypos "+tile+" "+startposy+")"))
        #breakpoint()
        self.kb.kb_retract(parse_input("fact: (xpos empty "+endposx+")"))
        #breakpoint()
        self.kb.kb_retract(parse_input("fact: (ypos empty "+endposy+")"))
        #assert new ones
        self.kb.kb_assert(parse_input("fact: (xpos "+tile+" "+endposx+")"))
        #breakpoint()
        self.kb.kb_assert(parse_input("fact: (ypos "+tile+" "+endposy+")"))
        #breakpoint()
        self.kb.kb_assert(parse_input("fact: (xpos empty "+startposx+")"))
        #breakpoint()
        self.kb.kb_assert(parse_input("fact: (ypos empty "+startposy+")"))
        return
        

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
