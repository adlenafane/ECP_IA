# -*- coding: utf-8 -*-
import socket
import struct
import sys
import time
from pprint import pprint
from threading import Timer
import config
import ai as ai
from conductor import Conductor
from utility import Board
import winsound

old_stdout = sys.stdout

log_file = open("./log/message"+str(int(round(time.time() * 1000)))+".log","w")
#log_file = open("./log/message.log","w")

sys.stdout = log_file


data = []
nb_tours = 0

stuxnet = ai.Stuxnet()
stuxnet_2 = ai.Stuxnet()
stuxnet_2.our_kind = config.eux_fixe
stuxnet_2.other_kind = config.nous_fixe

conductor = Conductor(stuxnet, stuxnet_2)

def send(sock, *messages):
    """Send a given set of messages to the server."""
    global data
    for message in messages:
        try:
            data = struct.pack('=B', message) if isinstance(message, int) else message
            #print data
            sock.send(data)
        except:
            print("Couldn't send message: ", message)

def send_order(sock, messages):
    """Send a given set of messages to the server."""
    global data
    for message in messages:
        try:
            data = struct.pack('=B', message) if isinstance(message, int) else message
            #print data
            sock.send(data)
        except:
            print("Couldn't send message: ", message)

def return_best_order(sock):
    best_move = config.best_move
    print "minmax return", best_move
    if best_move != []:
        order = best_move[1]
        print "order"
        if order != []:
            send_order(sock, order)
    config.nous = config.nous_fixe
    config.eux = config.eux_fixe

def beep(sound):
    winsound.PlaySound('sound/%s.wav' % sound, winsound.SND_FILENAME)

class Client():
    def __init__(self, Adress=("127.0.0.1",5555)):
        self.s = socket.socket()
        self.s.connect(Adress)

client = Client(config.address)
sock = client.s

#Envoi du nom
groupname = "Stuxnet - v0_8" #mettez ici le nom de votre equipe
send(sock, "NME", len(groupname), groupname)
print data
global home  #stock le tuple de coodonnees de notre maison. variable qui servira a identifier si on est des v ou des w
global Xsize
global Ysize

print "#################### fin de l'initialisation de la connexion ###################"
print "\n\n"

#boucle principale
while True:
    order = sock.recv(3)
    print order
    if not data:
        print("Bizarre, c'est vide. Aucun ordre n'a du etre envoyé au serveur au tour precedant")

    if order == "SET":
        global Xsize
        global Ysize
        lignes, colonnes = (struct.unpack('=B', sock.recv(1))[0] for i in range(2))   #B est le format pour unsigned char donc sock.recv(1) permet de lire 1 entier. The result of struct.unpack(format, string) is a tuple even if it contains exactly one item. l'opération est faite 2 fois pour récupérer ligne et colonne.
        #ici faire ce qu'il faut pour preparer votre representation de la carte
        Xsize = colonnes
        Ysize = lignes
        config.Xsize = Xsize
        config.Ysize = Ysize
        #(type,n): case occupée par n personnages de type:
                                #'h' pour les humains
                                #'v' pour les vampires
                                #'w' pour les loups garous

        print "#################### fin du SET ###################"
        print "\n\n"
        
    elif order == "HUM":
        n = struct.unpack('=B', sock.recv(1))[0]
        config.nb_of_h_positions_at_start = n
        print "reception de %i positions d'humains:" %n
        maisons = []
        for i in range(n):
            x,y=(struct.unpack('=B', sock.recv(1))[0] for i in range(2)) #on génere la liste de tuples de coordonnées des maisons (humains)
            maisons.append((x,y)) #on génere la liste de tuples de coordonnées
        print maisons
        #maisons contient la liste des coordonnees des maisons ajoutez votre code ici
        for maison in maisons:
            config.board[maison]=('h',0)
        print "Mise a jour du board: "
        pprint(config.board)
        print "\n\n"
        print "#################### fin du HUM ###################"
        print "\n\n"



    elif order == "HME":
        x, y = (struct.unpack('=B', sock.recv(1))[0] for i in range(2))
        #ajoutez le code ici (x,y) etant les coordonnees de votre maison
        config.board[(x,y)]=('nous',0)
        global home
        home=(x,y)
        print home
        print "#################### fin du HME ###################"
        print "\n\n"



    elif order == "UPD":
        nb_tours+=1
        n = struct.unpack('=B', sock.recv(1))[0]
        print "reception de %i changements dans le board:" %n
        changes = []
        for i in range(n):
            x,y,humanNB,vampNB,wwNB = (struct.unpack('=B', sock.recv(1))[0] for i in range(5))
            changes.append((x,y,humanNB,vampNB,wwNB))
        print changes 
        #initialisez votre carte a partir des tuples contenus dans changes
        for change in changes:
            if change[2]!=0:
                config.board[(change[0],change[1])]=('h', change[2])
            elif change[3]!=0:
                config.board[(change[0],change[1])]=('v', change[3])
            elif change[4]!=0:
                config.board[(change[0],change[1])]=('w', change[4])
            elif (change[2]==0 and change[3]==0 and change[4]==0):
                k = (change[0],change[1])
                try:
                    del config.board[k]
                except:
                    print "UPD a transmis une case vide qui etait deja vide"
            else:
                print "je n'ai pas compris l'ordre UPD"
        #pprint(config.board)

        current_board = Board(config.board, config.Xsize, config.Ysize)
        config.dominance = 1 if current_board.our_number() > current_board.ennemy_number() else 0

        #print "our_positions"
        #pprint(current_board.our_positions())
        #print "human_positions"
        #pprint(current_board.human_positions())
        #print "ennemy_positions"
        #pprint(current_board.ennemy_positions())

        # stuxnet.update_game_graph(current_board)
        
        #calculez votre coup
        
        our_timer=Timer(4.0, return_best_order, [sock])
        our_timer.start()
        conductor.minmax_smart(1, current_board)
        
        config.nous = config.nous_fixe
        config.eux = config.eux_fixe

        print "#################### fin du UPD ###################"
        print "\n\n"

    elif order == "MAP":
        n = struct.unpack('=B', sock.recv(1))[0]
        print "reception de %i changements dans le board:" %n
        changes = []
        creatures_on_board = 0
        for i in range(n):
            x,y,humanNB,vampNB,wwNB = (struct.unpack('=B', sock.recv(1))[0] for i in range(5))
            changes.append((x,y,humanNB,vampNB,wwNB))
            creatures_on_board += humanNB + vampNB + wwNB
        print changes
        #initialisez votre carte a partir des tuples contenus dans changes
        for change in changes:
            if change[2]!=0:
                config.board[(change[0],change[1])]=('h', change[2])
            elif change[3]!=0:
                config.board[(change[0],change[1])]=('v', change[3])
            elif change[4]!=0:
                config.board[(change[0],change[1])]=('w', change[4])
            elif (change[2]==0 and change[3]==0 and change[4]==0):
                k = (change[0],change[1])
                try:
                    del config.board[k]
                except:
                    print "UPD a transmis une case vide qui etait deja vide"
            else:
                print "je n'ai pas compris l'ordre MAP"

        config.nous = config.board[(home[0],home[1])] [0]  #enregistre 'v' ou 'w' dans la variable nous
        config.nous_fixe = config.nous
        if config.nous == 'v':
            config.eux = 'w'
            config.eux_fixe = config.eux
        else:
            config.eux = 'v'
            config.eux_fixe = config.eux

        stuxnet.our_kind = config.nous
        stuxnet.other_kind = config.eux
        print "nous sommes de type: %s" %config.nous
        pprint(config.board)

        #initialisation constante heuristique
        config.cst_heuri = creatures_on_board*100

        stuxnet.update_game_graph(Board(config.board, config.Xsize, config.Ysize))
        print "#################### fin du MAP ###################"
        print "\n\n"



    elif order == "END":
        if config.dominance == 1:
            beep('monsterkill')
        else:
            beep('holyshit')
        #ici on met fin a la partie en cours Reinitialisez votre modele
        break



    elif order == "BYE":
        break



    else:
        print("commande non attendue recue", order)

#Preparez ici la deconnexion
                


#Fermeture de la socket
sock.close()

sys.stdout = old_stdout

log_file.close()