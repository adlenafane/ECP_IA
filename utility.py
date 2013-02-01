# -*- coding: utf-8 -*-
from random import choice


# Coord1 et 2 sont des tuples ou des listes contenant x et y
def computeMinDistance(coord_1, coord_2):
    return max(abs(coord_2[0] - coord_1[0]), abs(coord_2[1] - coord_1[1]))

# Coord1 et 2 sont des tuples ou des listes contenant x et y
def findNextMove(coord_start, coord_goal):
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

def getOurPositions(board, nous):
    """
    entree: board, nous
    retourne: liste de tuples qui nous donne nos positions et notre nombre sur ces positions, la liste est classée par "nombre sur ces positions"
    """
    ourPositions =[]

    for k in board: 
        if board[k][0] == nous: 
            ourPositions.append((k, board[k][1]))
    
    return sorted(ourPositions, key=lambda position: position[1]) 



def anyEnnemyClose():
    """
    entree: board
    retourne: un dico avec en clé: tuple de positions des ennemis qui snt adjacents à une de nos positions, et en valeur un tuple (tuples de nos positions mmenacées, nombre de nos creatures présentes sur cette case)
    """

def anyHumanClose():
    """
    entree: board
    retourne: un dico avec en clé: tuple de positions des humains qui snt adjacents à une de nos positions, et en valeur un tuple (tuples de nos positions mmenacées, nombre de nos creatures présentes sur cette case)
    """

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

def next_coord(Xsize, Ysize, coord_start, direction):
    """
    coord_start est le tuple de coordonnes
    "direction" est une direction de deplacement. 8 possibilités: u,ur,r,dr,d,dl,l,ul
    si le mouvement dans cette diection est possible, retourne ls cordonnes suivantes apres le mouvement
    sinon retourne False
    """
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

def randomPossibleNextCoord(Xsize, Ysize, coord_start):
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
            coord = next_coord(Xsize, Ysize, coord_start, direction)
            print coord
    return coord