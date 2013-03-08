#Solves zero sum games
#Player -1 wants minimum score, player 1 wants maximum

ENDGAME = 10000


minmaxCache = {}
#Minmax cache keys are player,board
#The items are best score, next board, required depth
#Items only go into the cache if:
#  Guaranteed win/loss


minmaxHits = 0
minmaxMisses = 0

class Game:
    """Implements the functions needed to play a game"""


    def __init__(self):
        """Initializes board"""

    def makeMove(self, move, player):
        """Makes a move, where move is something returned from getNext"""

    def unmakeMove(self, move):
        """Returns board to state it was in before makeMove was called"""

    def score(self):
        """Returns a heuristic for the score of a game"""

    def getNext(self, player):
        """Returns generator of possible next states"""

    def printBoard(self):
        """Prints a board in some user friendly way"""

    def gameOver(self):
        if abs(self.score()) == ENDGAME:
            return True
        if len(tuple(self.getNext(-1)))==0:
            return True
        return False


class TicTacToe(Game):
    wins = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))

    def __init__(self):
        self.board = [0]*9

    def makeMove(self, move, player):
        self.board[move] = player

    def unmakeMove(self, move):
        self.board[move] = 0

    def win(self):
        for w in TicTacToe.wins:
            if self.board[w[0]]==self.board[w[1]]==self.board[w[2]]!=0:
                return self.board[w[0]]
        return False

    def score(self):
        winner = self.win()
        if winner:
            return ENDGAME*winner
        s = 0
        for i in xrange(9):
            if self.board[i]==0:
                self.board[i]=1
                if(self.win()):
                    s+=1
                self.board[i]=-1
                if(self.win()):
                    s-=1
                self.board[i]=0
        return s

    def getNext(self, player):
        for i, place in enumerate(self.board):
            if place==0:
                yield i
        
    def printBoard(self):
        for i in xrange(len(self.board)):
            print "%3d" % self.board[i],
            if (i+1)%3==0:
                print
        print '-----------------------------------'


class ConnectFour(Game):

    def __init__(self):
        self.board = [[0]*6 for _ in xrange(7)]

    def makeMove(self, move, player):
        place = self.board[move].index(0)
        self.board[move][place] = player

    def unmakeMove(self, move):
        try:
            place = self.board[move].index(0)-1
        except:
            place = len(self.board[move]) - 1
            
        self.board[move][place] = 0

    def score(self):
        result = [0]*9
        #Column
        for i in xrange(7):
            sum = self.board[i][0]+self.board[i][1]+self.board[i][2]
            for j in xrange(3,6):
                sum += self.board[i][j]
                result[sum+4]+=1
                sum -= self.board[i][j-3]

        #Row
        for j in xrange(6):
            sum = self.board[0][j]+self.board[1][j]+self.board[2][j]
            for i in xrange(3,7):
                sum += self.board[i][j]
                result[sum+4]+=1
                sum -= self.board[i-3][j]

        #Diagonal up right
        for i in xrange(4):
            for j in xrange(3):
                sum = 0
                for x in xrange(4):
                    sum += self.board[i+x][j+x]
                result[sum+4]+=1


        #Diagonal up left
        for i in xrange(3,7):
            for j in xrange(3):
                sum = 0
                for x in range(4):
                    sum += self.board[i-x][j+x]
                result[sum+4]+=1
    
        if result[0] != 0:
            return -ENDGAME
        elif result[8] != 0:
            return ENDGAME

        return -5*result[1] - 2*result[2] -result[3] + result[5] + 2*result[6] + 5*result[7] -10*result[0] + 10*result[8]

    def getNext(self, player):
        for num, column in enumerate(self.board):
            try:
                column.index(0) #Check if there is still a 0 in the colum
                yield num
            except:
                pass

    def printBoard(self):
        for i in xrange(6):
            for j in xrange(7):
                print "%3d" % self.board[j][5-i],
            print
        print '-----------------------------------'


def minmax(player, max_level=7, game = TicTacToe()):
    #Returns tuple (score, move, needed_depth)

    if max_level==0:
        return (game.score(),None, 0)

    cur_score = game.score()
    if abs(cur_score) == ENDGAME:
        return cur_score, None, 0

    nextMoves = game.getNext(player)

    bestScore = -ENDGAME*player
    needed_depth = max_level-1
    best = None

    for move in nextMoves:
        game.makeMove(move, player)
        curScore, curBest, curDepth = minmax(-player, needed_depth, game)
        if max_level == 6:
            print "Score for column %s: %s"%(move, curScore)
        if (player==-1 and curScore<bestScore) or (player==1 and curScore>bestScore) or (curScore==bestScore and curDepth<=needed_depth):
            best = move
            bestScore = curScore
            if bestScore*player == ENDGAME:
                needed_depth = curDepth
        game.unmakeMove(move)

    if best == None:
        return (game.score(),None, 0) #If game over, don't search deeper - return needed_depth of 0
    return bestScore, best, needed_depth+1

def playAgainst(game = TicTacToe()):
    computer = -1
    player = 1
    while not game.gameOver():
        game.makeMove(minmax(computer, 7, game = game)[1], computer)
        game.printBoard()
        if not game.gameOver():
            ###TODO:###
            ###General board input function
            ###
            move = -1
            while not (0 <= move <=8 and board[move]==0):
                move = int(raw_input("Make a move\n"))
            game.makeMove(move, player)
            game.printBoard()

def play(game = TicTacToe()):
    p1 = -1
    p2 =  1
    game.printBoard()
    if not game.gameOver():
        game.makeMove(minmax(p1, 6, game = game)[1], p1)
        game.printBoard()
        if not game.gameOver():
            game.makeMove(minmax(p2, 6, game = game)[1], p2)
            game.printBoard()




###Tests###

def testConnectFourScore():
    c = ConnectFour()
    winningBoards = [ [ [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        [1,1,1,1,0,0],
                        [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        [0,0,0,0,0,0] ],
                      
                      [ [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        [1,0,0,0,0,0],
                        [1,0,0,0,0,0],
                        [1,0,0,0,0,0],
                        [1,0,0,0,0,0],
                        [0,0,0,0,0,0] ],
                      
                      [ [0,0,0,1,0,0],
                        [0,0,1,0,0,0],
                        [0,1,0,0,0,0],
                        [1,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        [0,0,0,0,0,0] ],

                      [ [0,0,0,0,0,1],
                        [0,0,0,0,1,0],
                        [0,0,0,1,0,0],
                        [0,0,1,0,0,0],
                        [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        [0,0,0,0,0,0] ],

                      [ [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        [1,0,0,0,0,0],
                        [0,1,0,0,0,0],
                        [0,0,1,0,0,0],
                        [0,0,0,1,0,0] ],

                      [ [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        [0,0,1,0,0,0],
                        [0,0,0,1,0,0],
                        [0,0,0,0,1,0],
                        [0,0,0,0,0,1] ] ]

    for num, board in enumerate(winningBoards):
        c.board = board
        assert c.score() == ENDGAME

def test():
    testConnectFourScore()

if __name__ == "__main__":
    test()