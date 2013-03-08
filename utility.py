# -*- coding: utf-8 -*-
import config
from random import choice




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


def getOurPositions(any_board):
    """
    entree: board, nous
    retourne: liste de tuples qui nous donne nos positions et notre nombre sur ces positions
    NB: ne verifie pas la validite des coordonees
    """
    ourPositions =[]

    for k in any_board: 
        if any_board[k][0] == config.nous: 
            ourPositions.append((k, any_board[k][1]))

    return ourPositions

def getEnnemyPositions(any_board):
    """
    entree: board, 
    retourne: liste de tuples qui nous donne la position des ennemis et leur nombre sur ces positions
    NB: ne verifie pas la validite des coordonees
    """
    ennemyPositions = []
    for k in any_board:
        if any_board[k][0] == config.eux:
            ennemyPositions.append((k, any_board[k][1]))
    return ennemyPositions

def getHumanPositions(any_board):
    """
    entree: board
    retourne: liste de tuples qui nous donne la position des humains et leur nombre sur ces positions
    NB: ne verifie pas la validite des coordonees
    """
    humanPositions = []

    for k in any_board:
        if any_board[k][0] == 'h':
            humanPositions.append((k, any_board[k][1]))
    return humanPositions

def getHumanNumber(any_board): #to be checked
    """
    entree: board
    retourne le nombre d'humains restants sur le plateau
    """
    #rappel: board[(x,y)]=(type, nombre)
    return sum([v[1] for k,v in any_board.items() if v[0]=='h'])



def getOurNumber(any_board): #to be checked
    return sum([v[1] for k,v in any_board.items() if v[0]==config.nous])
 



def getEnnemyNumber(any_board): #to be checked
    """
    retourne le nombre d'ennemis restants sur le plateau
    """
    return sum([v[1] for k,v in any_board.items() if v[0]==config.eux])



def anyEnnemyClose(any_board):
    """
    retourne: un dico avec en clé: tuple de positions des ennemis qui snt adjacents à une de nos positions, et en valeur un tuple (tuples de nos positions mmenacées, nombre de nos creatures présentes sur cette case)
    """
    ourPositions = getOurPositions(any_board)
    ennemyPositions = getEnnemyPositions(any_board)
    allDistances = []
    for ourPosition in ourPositions:
        for ennemyPosition in ennemyPositions:
            distance = computeMinDistance(ourPosition[0], ennemyPosition[0])
            allDistances.append((ourPosition, ennemyPosition, distance))
    return sorted(allDistances, key=lambda distance: distance[2])



def anyHumanClose(any_board):
    """
    retourne: un dico avec en clé: tuple de positions des humains qui snt adjacents à une de nos positions, et en valeur un tuple (tuples de nos positions mmenacées, nombre de nos creatures présentes sur cette case)
    """
    ourPositions = getOurPositions(any_board)
    humanPositions = getHumanPositions(any_board)
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



def sum_min_distance_us_human_delta(any_board):
    dist = 0
    our_positions = getOurPositions(any_board) #[((x,y),number)]
    human_positions = get_human_positions(any_board) #[((x,y),number)]
    for our_position in our_positions:
        local_dist= +inf
        local_coef=0 #will be set to +1 if humans outnumber us
        for human_position in human_positions:
            if computeMinDistance(our_position[0],human_position[0]) < local_dist:
                local_dist = computeMinDistance(our_position[0],human_position[0])
                if our_position[1]<human_position[1]:
                    local_coef = 1
                else:
                    local_coef = -1
        dist+=local_dist*local_coef
    return dist



def sum_min_distance_us_ennemy_delta(any_board):
    dist = 0
    our_positions = getOurPositions(any_board) #[((x,y),number)]
    ennemy_positions = get_ennemy_positions(any_board) #[((x,y),number)]
    for our_position in our_positions:
        local_dist= +inf
        local_coef=0 #will be set to -1 if ennemies outnumber us
        for ennemy_position in ennemy_positions:
            if computeMinDistance(our_position[0],ennemy_position[0]) < local_dist:
                local_dist = computeMinDistance(our_position[0],ennemy_position[0])
                if our_position[1]<ennemy_position[1]:
                    local_coef = -1
                else:
                    local_coef = +1
        dist+=local_dist*local_coef
    return dist



def sum_min_distance_ennemy_human_delta(any_board):
    dist = 0
    ennemy_positions = get_ennemy_positions(any_board) #[((x,y),number)]
    human_positions = get_human_positions(any_board) #[((x,y),number)]
    for ennemy_position in ennemy_positions:
        local_dist= +inf
        local_coef=0 #will be set to +1 if humans outnumber ennemies
        for human_position in human_positions:
            if computeMinDistance(ennemy_position[0],human_position[0]) < local_dist:
                local_dist = computeMinDistance(ennemy_position[0],human_position[0])
                if ennemy_position[1]<human_position[1]:
                    local_coef = 1
                else:
                    local_coef = -1
        dist+=local_dist*local_coef
    return dist



def heuristic_delta(ennemy_number_delta, our_number_delta,human_number_delta, sum_min_distance_us_human_delta, sum_min_distance_us_ennemy_delta, sum_min_distance_ennemy_human_delta):
    """
    positive = favorable
    """
    return (30*our_number_delta - 20*ennemy_number_delta - 10*human_number_delta - sum_min_distance_us_human_delta + sum_min_distance_us_ennemy_delta + sum_min_distance_ennemy_human_delta)



def compute_human_targets(any_board):
    """
    
    """
    human_positions = get_human_positions(any_board) #[((x,y),number)]
    our_positions = getOurPositions(any_board)
    human_targets=[] #de la forme [((x,y),nombre,distance min à notre position, notre nombre sur cette position]
    for human_position in human_positions:
        for our_position in our_positions:
            human_targets.append((human_position[0],human_position[1],computeMinDistance(human_positions[0],our_position[0]),our_position[1]))

    


def go_attack_ennemies(any_board, position):
    """

    """

