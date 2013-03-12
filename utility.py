# -*- coding: utf-8 -*-
import config
from random import choice
import math



def computeMinDistance(coord_1, coord_2):
    """
    Coord1 et 2 sont des tuples ou des listes contenant x et y
    """
    return max(abs(coord_2[0] - coord_1[0]), abs(coord_2[1] - coord_1[1]))


def findNextMove(coord_start, coord_goal):
    """
    entrees: une coordonee de depart et une coordonee cible, qui sont des tuples ou des listes contenant x et y
    retourne: la prochaine case sur laquelle aller
    """
    if coord_start[0] == coord_goal[0] and coord_start[1] == coord_goal[1]:
        return (coord_start)
    elif coord_start[0] == coord_goal[0]:
        if coord_start[1] < coord_goal[1]:
            return (coord_start[0], coord_start[1]+1)
        else:
            return (coord_start[0], coord_start[1]-1)
    elif coord_start[1] == coord_goal[1]:
        if coord_start[0] < coord_goal[0]:
            return (coord_start[0]+1, coord_start[1])
        else:
            return (coord_start[0]-1, coord_start[1])
    elif coord_start[0] < coord_goal[0]:
        if coord_start[1] < coord_goal[1]:
            return (coord_start[0]+1, coord_start[1]+1)
        else:
            return (coord_start[0]+1, coord_start[1]-1)
    elif coord_start[0] > coord_goal[0]:
        if coord_start[1] < coord_goal[1]:
            return (coord_start[0]-1, coord_start[1]+1)
        else:
            return (coord_start[0]-1, coord_start[1]-1)





def attack(targetPosition):
    """
    entree: tuple de coordonnes de la cellule a attaquer et board
    nb: faire un test si la cellule cible est bien une cellule a notre portee
    retourne: le send correctement formaté
    """
    adjacentsList=getAdjacentPositions(targetPosition)
    if checkPresence(adjacentsList,config.board)==False:
        return "Cellule hors de portee"
    else:
        #Lancer ordre attaque
        return send(sock,"ATK",targetPosition[0],targetPosition[1])

def checkPresence(adjacentsList):
    """
    Entree: liste de tuples de positions
    Sortie: True ou False selon presence de nous dans au moins une de ces cases
    """
    for tuplePosition in adjacentsList:
        if tuplePosition in config.board:
            if tuplePosition[0]==config.nous:
                return True
    return False

def getAdjacentPositions(targetPosition):
    """
    Entree: tuple de position
    Sortie: liste de tuples des cases adjacentes
    """
    xmax=config.Xsize
    ymax=config.Ysize
    result=[]
    if (targetPosition[0] not in [0,xmax-1]) and (targetPosition[1] not in [0,ymax-1]):
        return []
    elif targetPosition[0]==0:
        pass

def move(coord_start,number,coord_end):
    """
    entree: une liste de quintuplets
    NB: checker ue le nombre de quintuplets est < à 3
    retourne: le send correctement formaté
    """
    return send(sock, "MOV", coord_start[0], coord_start[1], number,coord_end[0],coord_end[1])

def next_coord(coord_start, direction):
    """
    coord_start est le tuple de coordonnes
    "direction" est une direction de deplacement. 8 possibilités: u,ur,r,dr,d,dl,l,ul
    si le mouvement dans cette diection est possible, retourne ls cordonnes suivantes apres le mouvement
    sinon retourne False
    """

    Xsize = config.Xsize
    Ysize = config.Ysize

    if direction == 'u':
        print "direction u"
        if coord_start[1]+1<=Ysize-1:
            return (coord_start[0], coord_start[1]+1)
        else:
            return coord_start

    elif direction == 'ur':
        if coord_start[0]+1<=Xsize-1 and coord_start[1]+1<=Ysize-1 :
            return (coord_start[0]+1, coord_start[1]+1)
        else:
            return coord_start

    elif direction == 'r':
        if coord_start[0]+1<=Xsize-1:
            return (coord_start[0]+1, coord_start[1])
        else:
            return coord_start
   

    elif direction == 'dr':
        if coord_start[0]+1<=Xsize-1 and coord_start[1]-1>=0:
            return (coord_start[0]+1, coord_start[1]-1)
        else:
            return coord_start
   

    elif direction == 'd':
        if coord_start[1]-1>=0:
            return (coord_start[0], coord_start[1]-1)
        else:
            return coord_start
   

    elif direction == 'dl':
        if coord_start[0]-1>=0 and coord_start[1]-1>=0:
            return (coord_start[0], coord_start[1]-1)
        else:
            return coord_start
   

    elif direction == 'l':
        if coord_start[0]-1>=0:
            return (coord_start[0], coord_start[1])
        else:
            return coord_start
   

    elif direction == 'ul':  
        if coord_start[0]-1>=0 and coord_start[1]+1<=Ysize-1:
            return (coord_start[0]-1, coord_start[1]+1)
        else:
            return coord_start




def randomPossibleNextCoord(coord_start):
    """
    Renvoie les coordonnées possibles (= qui ne sort pas de la carte) pour un next move aléatoire. 
    """
    print "\nProcedure randomPossibleNextCoord"
    coord=coord_start
    print coord
    while (coord==coord_start):
            print "debut d'une boucle de while"
            direction= choice(['u','ur','r','dr','d','dl','l','ul'])
            print direction
            coord = next_coord(coord_start, direction)
            print coord
    return coord



    


def go_attack_ennemies(any_board, position):
    """

    """

class VectorPosition():
    def __init__(self, kind, coord, number):
        self.kind = kind   # 'v', 'w' or 'h'
        self.coord = coord
        self.number = number
"""
    def kind(self):
        return self.kind

    def coord(self):
        return self.coord

    def number(self):
        return self.number"""



class Board():
    """ Class to handle boards"""
    def __init__(self,grid,x,y):
        #print '\n'+50*'#'+"Board::__init__"+str(grid)+str(x)+str(y)
        self.grid = grid  #{coord:(kind,number)}
        self.x_max = x
        self.y_max = y

    def our_positions(self):
        """
        formerly getour_positions(any_board)
        entree: board, nous
        retourne: liste de tuples qui nous donne nos positions et notre nombre sur ces positions
        NB: ne verifie pas la validite des coordonees
        """
        #print '\n'+50*'#'+"Board::our_positions()"
        our_positions =[]

        for k in self.grid.keys(): 
            if self.grid[k][0] == config.nous: 
                our_positions.append(VectorPosition(self.grid[k][0],k,self.grid[k][1]))
        return our_positions


    def ennemy_positions(self):
        """
        formerly getEnnemyPositions(any_board)
        entree: board, 
        retourne: liste de tuples qui nous donne la position des ennemis et leur nombre sur ces positions
        NB: ne verifie pas la validite des coordonees
        """
        #print '\n'+50*'#'+"Board::ennemy_positions()"
        ennemy_positions = []
        for k in self.grid.keys(): 
            if self.grid[k][0] == config.eux: 
                ennemy_positions.append(VectorPosition(self.grid[k][0],k,self.grid[k][1]))
        return ennemy_positions


    def human_positions(self):
        """
        formerly gethuman_positions(any_board)
        entree: board
        retourne: liste de tuples qui nous donne la position des humains et leur nombre sur ces positions
        NB: ne verifie pas la validite des coordonees
        """
        #print '\n'+50*'#'+"Board::human_positions()"
        human_positions = []
        for k in self.grid.keys(): 
            if self.grid[k][0] == 'h': 
                human_positions.append(VectorPosition(self.grid[k][0],k,self.grid[k][1]))
        return human_positions

    def human_number(self): #to be checked
        """
        formerly getHumanNumber(any_board)
        entree: board
        retourne le nombre d'humains restants sur le plateau
        """
        #print '\n'+50*'#'+"Board::human_number()"
        #rappel: board[(x,y)]=(type, nombre)
        return sum([v[1] for k,v in self.grid.items() if v[0]=='h'])



    def our_number(self): #to be checked
        """
        formerly getOurNumber(any_board)
        """
        #print '\n'+50*'#'+"Board::our_number()"
        return sum([v[1] for k,v in self.grid.items() if v[0]==config.nous])

    def ennemy_number(self): #to be checked
        """
        formerly getEnnemyNumber(any_board) 
        retourne le nombre d'ennemis restants sur le plateau
        """
        #print '\n'+50*'#'+"Board::ennemy_number()"
        return sum([v[1] for k,v in self.grid.items() if v[0]==config.eux])



    def ennemy_close(self):
        """
        formerly anyEnnemyClose(any_board)
        retourne: un dico avec en clé: tuple de positions des ennemis qui snt adjacents à une de nos positions, et en valeur un tuple (tuples de nos positions mmenacées, nombre de nos creatures présentes sur cette case)
        """
        #print '\n'+50*'#'+"Board::ennemy_close()"
        our_positions = self.our_positions()
        ennemy_positions = self.ennemy_positions()
        allDistances = []
        for our_position in our_positions:
            for ennemy_position in ennemy_positions:
                distance = computeMinDistance(our_position.coord, ennemy_position.coord)
                allDistances.append((our_position, ennemy_position, distance))
        return sorted(allDistances, key=lambda distance: distance[2])



    def human_close(self):
        """
        formerly anyHumanClose(any_board)
        retourne: un dico avec en clé: tuple de positions des humains qui snt adjacents à une de nos positions, et en valeur un tuple (tuples de nos positions mmenacées, nombre de nos creatures présentes sur cette case)
        """
        #print '\n'+50*'#'+"Board::human_close()"
        our_positions = self.our_positions()
        human_positions = self.human_positions()
        allDistances = []
        for our_position in our_positions:
            for human_position in human_positions:
                distance = computeMinDistance(our_position.coord, human_position.coord)
                allDistances.append((our_position, human_position, distance))
        return sorted(allDistances, key=lambda distance: distance[2])



    def sum_min_distance_us_human_delta(self):
        """
        formerly sum_min_distance_us_human_delta(any_board)
        """
        #print '\n'+50*'#'+"Board::sum_min_distance_us_human_delta()"
        dist = 0
        our_positions = self.our_positions() #[((x,y),number)]
        human_positions = self.human_positions() #[((x,y),number)]
        if human_positions:
            for our_position in our_positions:
                local_dist= float("inf")
                local_coef=0 #will be set to +1 if humans outnumber us
                for human_position in human_positions:
                    if computeMinDistance(our_position.coord,human_position.coord) < local_dist:
                        local_dist = computeMinDistance(our_position.coord,human_position.coord)
                        if our_position.number<=human_position.number:
                            local_coef = 1
                        else:
                            local_coef = -1
                dist+=local_dist*local_coef
        return dist



    def sum_min_distance_us_ennemy_delta(self):
        """
        formerly sum_min_distance_us_ennemy_delta(any_board)
        """
        #print '\n'+50*'#'+"Board::sum_min_distance_us_ennemy_delta()"
        dist = 0
        our_positions = self.our_positions() #[((x,y),number)]
        ennemy_positions = self.ennemy_positions() #[((x,y),number)]

        if ennemy_positions:
            for our_position in our_positions:
                local_dist= float("inf")
                local_coef=0 #will be set to -1 if ennemies outnumber us
                for ennemy_position in ennemy_positions:
                    if computeMinDistance(our_position.coord,ennemy_position.coord) < local_dist:
                        local_dist = computeMinDistance(our_position.coord,ennemy_position.coord)
                        if our_position.number<ennemy_position.number:
                            local_coef = -1
                        else:
                            local_coef = +1
                dist+=local_dist*local_coef
        return dist



    def sum_min_distance_ennemy_human_delta(self):
        """
        formerly sum_min_distance_ennemy_human_delta(any_board)
        """
        #print '\n'+50*'#'+"Board::sum_min_distance_ennemy_human_delta()"
        dist = 0
        ennemy_positions = self.ennemy_positions()
        human_positions = self.human_positions()
        if human_positions:
            for ennemy_position in ennemy_positions:
                local_dist= float("inf")
                local_coef=0 #will be set to +1 if humans outnumber ennemies
                for human_position in human_positions:
                    if computeMinDistance(ennemy_position.coord,human_position.coord) < local_dist:
                        local_dist = computeMinDistance(ennemy_position.coord,human_position.coord)
                        if ennemy_position.number<human_position.number:
                            local_coef = 1
                        else:
                            local_coef = -1
                dist+=local_dist*local_coef
        return dist



    def score(self):
        """
        positive = favorable
        """
        #print '\n'+50*'#'+"Board::score()"
        k = config.cst_heuri

        #constante de domination
        if self.our_number()>=self.ennemy_number():
            dominance=1
        else:
            dominance = 0

        # Anti-suicide fix :)
        if self.our_number() == 0:
            return -k
        if self.ennemy_number() == 0:
            return k
        # - 20*self.human_number()

        return (k \
            + 20*self.our_number() \
            - 21*self.ennemy_number()  \
            - self.sum_min_distance_us_human_delta() \
            + self.sum_min_distance_us_ennemy_delta() \
            + self.sum_min_distance_ennemy_human_delta() \
            + dominance*50.0*1.0/(0.1+1.0/5*self.human_number())*self.our_number()/len(self.our_positions()))  \
            + (1-dominance)*50.0*1.0/(0.1+1.0/5*self.human_number())*len(self.our_positions())/self.our_number())




    def human_targets(self):
        """
        
        """
        #print '\n'+50*'#'+"Board::human_targets()"
        human_positions = self.grid.human_positions() 
        our_positions = self.grid.our_positions() 
        human_targets=[] #de la forme [((x,y),nombre,distance min à notre position, notre nombre sur cette position]
        for human_position in human_positions:
            for our_position in our_positions:
                human_targets.append((human_position.coord,human_position.number,computeMinDistance(human_positions[0],our_position.coord),our_position.number))


def main():
    """
    for testing purposes only
    this part is executed only when the file is executed in command line 
    (ie not executed when imported in another file)
    """
    grid = {(0,0):('h',5),(2,5):('v',4),(1,4):('w',3),(4,3):('h',2),(5,0):('h',3),(2,2):('v',4),(4,8):('w',5),(8,8):('w',2),(5,9):('v',4)}

    config.nous = 'v'
    config.eux = 'w'

    v = VectorPosition('v', (5,0),4)
    print v.coord


    #instanciate a board:
    board = Board(grid,10,10)

    #test methods:
    print '-'*50
    print "Nombre de nos creatures: "+str(board.our_number())
    print "Nombre d'humains: "+str(board.human_number())
    print "Nombre d'ennemis: "+str(board.ennemy_number())
    print '-'*50
    print "Nos positions: " + str(board.our_positions())
    print "Notre premiere position: "+str(board.our_positions()[0])
    print "Les coordonnees de notre premiere position: "+str((board.our_positions()[0]).coord)
    print '-'*50
    print "Nos ennemis proches sont: " + str(board.ennemy_close())
    print "Les humains proches sont: " + str(board.human_close())
    print '-'*50
    print "le score heuristique du board est: "+str(board.score())


#for testing purposes only
if __name__=="__main__":
    main()