# -*- coding: utf-8 -*-
import config
from random import choice

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

def getHumanNumber(): #to be checked
    """
    entree: board
    retourne le nombre d'humains restants sur le plateau
    """
    #rappel: board[(x,y)]=(type, nombre)
    return sum([v[1] for k,v in config.board.items() if v[0]=='h'])


def getOurNumber(): #to be checked
    """
    entree: board
    retourne le nombre d'humains restants sur le plateau
    """
    #rappel: board[(x,y)]=(type, nombre)
    return sum([v[1] for k,v in config.board.items() if v[0]==config.nous])


def getEnnemyNumber(): #to be checked
    """
    entree: board, nous
    nous='v' ou 'w' 
    retourne le nombre d'ennemis restants sur le plateau
    """
    if config.nous == 'v':
        ennemy_type='w'
    else:
        ennemy_type='v'
    return sum([v[1] for k,v in config.board.items() if v[0]==ennemy_type])

def get_heuristic_score():
    """
    entree: board, nous
    nous='v' ou 'w' 
    retourne un entier représentant le score heuristique du board
    Plus le score est élevé, plus le board nous est favorable
    Valeurs des coefficients à tester
    """
    return 3*getOurNumber(config.board, config.nous) - 2*getEnnemyNumber(config.board, config.nous) - getHumanNumber(config.board)

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
            coord = next_coord(config.Xsize, config.Ysize, coord_start, direction)
            print coord
    return coord