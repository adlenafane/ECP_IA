# -*- coding: utf-8 -*-
import config

# Coord1 et 2 sont des tuples ou des listes contenant x et y
def computeMinDistance(coord_1, coord_2):
    """
    entrees: une coordonee de depart et une coordonee cible
    retourne: La distance optimale entre ces 2 coordonees
    NB: ne verifie pas la validite des coordonees
    """
    return max(abs(coord_2[0] - coord_1[0]), abs(coord_2[1] - coord_1[1]))

# Coord1 et 2 sont des tuples ou des listes contenant x et y
def findNextMove(coord_start, coord_goal):
    """
    entrees: une coordonee de depart et une coordonee cible
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

def getOurPositions():
    """
    entree: board, nous
    retourne: liste de tuples qui nous donne nos positions et notre nombre sur ces positions
    NB: ne verifie pas la validite des coordonees
    """
    ourPositions =[]

    for k in config.board: 
        if config.board[k][0] == config.nous: 
            ourPositions.append((k, config.board[k][1]))

    return ourPositions

def getEnnemyPositions():
    """
    entree: board, 
    retourne: liste de tuples qui nous donne la position des ennemis et leur nombre sur ces positions
    NB: ne verifie pas la validite des coordonees
    """
    ennemyPositions = []
    for k in config.board:
        if config.board[k][0] == config.eux:
            ennemyPositions.append((k, config.board[k][1]))
    return ennemyPositions

def getHumanPositions():
    """
    entree: board
    retourne: liste de tuples qui nous donne la position des humains et leur nombre sur ces positions
    NB: ne verifie pas la validite des coordonees
    """
    humanPositions = []

    for k in config.board:
        if config.board[k][0] == 'h':
            humanPositions.append((k, config.board[k][1]))
    return humanPositions

def anyEnnemyClose():
    """
    entree: board
    retourne: un dico avec en clé: tuple de positions des ennemis qui snt adjacents à une de nos positions, et en valeur un tuple (tuples de nos positions mmenacées, nombre de nos creatures présentes sur cette case)
    """
    ourPositions = getOurPositions()
    ennemyPositions = getEnnemyPositions()
    allDistances = []
    for ourPosition in ourPositions:
        for ennemyPosition in ennemyPositions:
            distance = computeMinDistance(ourPosition[0], ennemyPosition[0])
            allDistances.append((ourPosition, ennemyPosition, distance))
    return sorted(allDistances, key=lambda distance: distance[2])

def anyHumanClose():
    """
    entree: board
    retourne: un dico avec en clé: tuple de positions des humains qui snt adjacents à une de nos positions, et en valeur un tuple (tuples de nos positions mmenacées, nombre de nos creatures présentes sur cette case)
    """
    ourPositions = getOurPositions()
    humanPositions = getHumanPositions()
    allDistances = []
    for ourPosition in ourPositions:
        for humanPosition in humanPositions:
            distance = computeMinDistance(ourPosition[0], humanPosition[0])
            allDistances.append((ourPosition, humanPosition, distance))
    return sorted(allDistances, key=lambda distance: distance[2])


def attack():
    """
    entree: tuple de coordonnes de la cellule a attaquer
    nb: faire un test si la cellule cible est bien une cellule a notre portee
    retourne: le send correctement formaté
    """

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
