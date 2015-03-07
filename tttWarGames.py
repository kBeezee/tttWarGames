import sys
import random as r
'''
http://en.wikipedia.org/wiki/WarGames

http://ostermiller.org/tictactoeexpert.html
The above describes the different ways to play tic tac toe:
    1. The Novice player makes random moves
    2. The Intermediate player will blocks their opponent from winning (and purposely win games)
    3. The Experienced player knows that playing in certain first squares will lose the game
    4. The Expert player will never lose

    todo:
    Expert
'''
hGames = [0, 0, 0] #x/o/d

###STATS ONLY NOT GAME RELATED
def RecordGame(outcome):
    if outcome == 'x':
        hGames[0] += 1
    elif outcome == 'o':
        hGames[1] += 1
    else:
        hGames[2] += 1
###############################

class tttAI():
    def __init__(self):
        pass
    

def Novice(gObj, MyTurn):
    x = r.randint(0, 2)
    y = r.randint(0, 2)
    while gObj.Board[x][y] != 0:
        x = r.randint(0, 2)
        y = r.randint(0, 2)
    gObj.Board[x][y] = MyTurn
    return

def Intermediate(gObj, MyTurn):
    if MyTurn == 'x':
        Enemy = 'o'
    elif MyTurn == 'o': #
        Enemy = 'x'
    else:
        sys.exit(MyTurn, ' Passed to Intermediate; Exiting.')

    (oMove, pMove) = (9, 9)
    #search for a move that will make my ($MyTurn) enemy win
    #print (oMove, pMove)
    (oMove, pMove) = gObj.getBlocksFor(Enemy)
    if (oMove, pMove) != (9, 9):
        gObj.Board[oMove][pMove] = MyTurn
        return

    #search for a move that will make my ($MyTurn) enemy win
    #print (oMove, pMove)
    (oMove, pMove) = gObj.getBlocksFor(MyTurn)
    if (oMove, pMove) != (9, 9):
        gObj.Board[oMove][pMove] = MyTurn
        return

    #print (oMove, pMove)
    #no blocks, place a random
    if (oMove, pMove) == (9, 9):
        Novice(gObj, MyTurn)
        return


def Experienced(gObj, MyTurn):
    if MyTurn == 'x':
        Enemy = 'o'
    elif MyTurn == 'o': #
        Enemy = 'x'
    else:
        sys.exit(MyTurn, ' Passed to Experienced; Exiting.')

    (oMove, pMove) = (9, 9)
    #1st move of the game; always choose center first.
    if gObj.GameStatus[2] == 9 and gObj.GameStatus[1] == 0 and gObj.GameStatus[0] == 0:
        gObj.Board[1][1] = MyTurn
        return

    #2nd move of the game
    if gObj.GameStatus[2] == 8 and gObj.GameStatus[0] == 1 and gObj.GameStatus[1] == 0:
        if gObj.Board[1][1] == 0:
            gObj.Board[1][1] = MyTurn
            return
        else:  # 2nd move of the game; but middle is taken, choose a 'random' corner, or in this case Top Left, (0, 0)
            gObj.Board[0][0] = MyTurn
            return

    Intermediate(gObj, MyTurn)
    return

def Expert(gObj, MyTurn):
    pass


class tttGame():
    def __init__(self, xSkills=2, oSkills=2):
        self.Board = [[0 for x in range(3)] for x in range(3)]
        self.GameStatus = [0, 0, 9]
        self.xSkills = xSkills
        self.oSkills = oSkills

    def display(self):
        for x in range(3):
            for y in range(3):
                if self.Board[x][y] == 0:
                    sys.stdout.write(" ")
                else: #x or o
                    sys.stdout.write(str(self.Board[x][y]))
            print("")

    def getBlocksFor(self, bMyTurn):
        if bMyTurn == 'o':
            enemy = 'x'
        elif bMyTurn == 'x':
            enemy = 'o'
        else:
            sys.exit(bMyTurn, ': Invalid parg passed to getBlocksFor()')
    #diags
        if enemy == self.Board[0][0] == self.Board[1][1] and self.Board[2][2] == 0:
            return (2, 2)
        if enemy == self.Board[0][0] == self.Board[2][2] and self.Board[1][1] == 0:
            return (1, 1)
        if enemy == self.Board[1][1] == self.Board[2][2] and self.Board[0][0] == 0:
            return (0, 0)

        if enemy == self.Board[0][2] == self.Board[1][1] and self.Board[2][0] == 0:
            return (2, 0)
        if enemy == self.Board[0][2] == self.Board[2][0] and self.Board[1][1] == 0:
            return (1, 1)
        if enemy == self.Board[2][0] == self.Board[1][1] and self.Board[0][2] == 0:
            return (0, 2)
    #horz
        for j in range(3):
            if enemy == self.Board[j][0] == self.Board[j][1] and self.Board[j][2] == 0:
                return (j, 2)
            if enemy == self.Board[j][0] == self.Board[j][2] and self.Board[j][1] == 0:
                return (j, 1)
            if enemy == self.Board[j][1] == self.Board[j][2] and self.Board[j][0] == 0:
                return (j, 0)

    #vert -- Do i need another for statement here?
            if enemy == self.Board[0][j] == self.Board[1][j] and self.Board[2][j] == 0:
                return (2, j)
            if enemy == self.Board[0][j] == self.Board[2][j] and self.Board[1][j] == 0:
                return (1, j)
            if enemy == self.Board[1][j] == self.Board[2][j] and self.Board[0][j] == 0:
                return (0, j)
        return (9, 9)

    def refreshGameStatus(self):
        xCount = oCount = eCount = 0
        for x in range(3):
            for y in range(3):
                if self.Board[x][y] == 'x':
                    xCount += 1
                elif self.Board[x][y] == 'o':
                    oCount += 1
                elif self.Board[x][y] == 0:
                    eCount += 1
                else:
                    sys.exit('invalid char on board.')
        self.GameStatus = [xCount, oCount, eCount]

    def isWinner(self):
        #horizontal line
        for x in range(3):
            if self.Board[x][0] == self.Board[x][1] == self.Board[x][2] != 0:
                return self.Board[x][0]
        #vertical line
        for x in range(3):
            if self.Board[0][x] == self.Board[1][x] == self.Board[2][x] != 0:
                return self.Board[0][x]
        #diags
        if self.Board[0][0] == self.Board[1][1] == self.Board[2][2] != 0:
            return self.Board[1][1]
        if self.Board[0][2] == self.Board[1][1] == self.Board[2][0] != 0:
            return self.Board[1][1]

    def taketurn(self):
        #whos turn is it?
        #is it the first move?
        if self.GameStatus[2] == 9:
            WhoseTurn = 'x'
            skilllevel = self.xSkills
        #moves left is not even, x goes
        elif self.GameStatus[2] % 2 != 0:
            WhoseTurn = 'x'
            skilllevel = self.xSkills
        #moves left is even, o goes
        else:
            WhoseTurn = 'o'
            skilllevel = self.oSkills

        #take your turn
        if skilllevel == 3:
            pass #expert
        elif skilllevel == 2:
            Experienced(self, WhoseTurn)
        elif skilllevel == 1:
            Intermediate(self, WhoseTurn)
        else:
            Novice(self, WhoseTurn)

        #refresh game status
        self.refreshGameStatus()

    def PlayUntilEnd(self, DisplayEachTurn = False, DisplayAtEndOfGame = True):
        while self.isWinner() is None and self.GameStatus[2] > 0:
            #print self.GameStatus
            self.taketurn()
            if DisplayEachTurn == True:
                self.display()
                print "-----"

        if DisplayAtEndOfGame != False:
            self.display()
            print "---"
        return self.isWinner()

for i in range(100):
    currentGame = tttGame(2, 2)
    RecordGame(currentGame.PlayUntilEnd(False, False))
    currentGame = None

print '|X  O  D|'
print hGames