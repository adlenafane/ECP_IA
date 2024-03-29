# -*- coding: utf-8 -*-
import socket, struct
from pprint import pprint


data = []
nb_tours = 0
def send(sock, *messages):
    """Send a given set of messages to the server."""
    global data
    for message in messages:
        try:
            data = struct.pack('=B', message) if isinstance(message, int) else message
            print data
            sock.send(data)
        except:
            print("Couldn't send message: ", message)


class Client():
    def __init__(self, Adress=("127.0.0.1",5555)):
        self.s = socket.socket()
        self.s.connect(Adress)

client = Client()
sock = client.s

#Envoi du nom
groupname = "Stuxnet" #mettez ici le nom de votre equipe
send(sock, "NME", len(groupname), groupname)
print data
global home  #stock le tuple de coodonnees de notre maison. variable qui servira a identifier si on est des v ou des w
global nous  #variable qui contiendra 'v' si on est des v ou 'w' si on est des w
print "#################### fin de l'initialisation de la connexion ###################"
print "\n\n"


#boucle principale
while True:
    order = sock.recv(3)
    print order
    if not data:
        print("Bizarre, c'est vide")

    if order == "SET":
        lignes, colonnes = (struct.unpack('=B', sock.recv(1))[0] for i in range(2))   #B est le format pour unsigned char donc sock.recv(1) permet de lire 1 entier. The result of struct.unpack(format, string) is a tuple even if it contains exactly one item. l'opération est faite 2 fois pour récupérer ligne et colonne.
        #ici faire ce qu'il faut pour preparer votre representation de la carte
        board = [[(0,0)]*colonnes for _ in range(lignes)]
        pprint(board)
        #(0,0): cases vides
        #(type,n): case occupée par n personnages de type:
                                #'h' pour les humains
                                #'v' pour les vampires
                                #'w' pour les loups garous
        print "#################### fin du SET ###################"
        print "\n\n"
        
    elif order == "HUM":
        n = struct.unpack('=B', sock.recv(1))[0]
        print "reception de %i positions d'humains:" %n
        maisons = []
        for i in range(n):
            x,y=(struct.unpack('=B', sock.recv(1))[0] for i in range(2)) #on génere la liste de tuples de coordonnées des maisons (humains)
            maisons.append((x,y)) #on génere la liste de tuples de coordonnées
        print maisons
        #maisons contient la liste des coordonnees des maisons ajoutez votre code ici
        for maison in maisons:
            board[maison[1]][maison[0]]=('h',0)
            pprint(board)
        print "\n\n"
        print "#################### fin du HUM ###################"
        print "\n\n"



    elif order == "HME":
        x, y = (struct.unpack('=B', sock.recv(1))[0] for i in range(2))
        #ajoutez le code ici (x,y) etant les coordonnees de votre maison
        board[y][x]=('nous',0)
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
                board[change[1]][change[0]]=('h', change[2])
            elif change[3]!=0:
                board[change[1]][change[0]]=('v', change[3])
            elif change[4]!=0:
                board[change[1]][change[0]]=('w', change[4])
            elif (change[2]==0 and change[3]==0 and change[4]==0):
                board[change[1]][change[0]]=(0,0)
            else:
                print "je n'ai pas compris l'ordre UPD"
        pprint(board)

        #calculez votre coup
        #calculcoup(board,nous,nb_tours)


        #preparez la trame MOV ou ATK
        #Par exemple: un ordre MOV qui fonctionne mais "ne respecte pas les regles" (je sais pas pk)
        send(sock, "MOV", 2,5,4,2,4,4,5,4,1,5,3) #arg: "MOV" est suivi du nombre de quintuplets de deplacement n, puis des n quintuplets: (Xdepart, Ydepart, nb de pers a deplacer, X arrivee, Y arrivee)
        
        #un ex d'ordre ATK qui fonctionne:
        #send(sock, "ATK",4,4) #arg: "ATK" suivi des coordonnées de la cellule cible
        print "#################### fin du UPD ###################"
        print "\n\n"

    elif order == "MAP":
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
                board[change[1]][change[0]]=('h', change[2])
            elif change[3]!=0:
                board[change[1]][change[0]]=('v', change[3])
            elif change[4]!=0:
                board[change[1]][change[0]]=('w', change[4])
            elif (change[2]==0 and change[3]==0 and change[4]==0):
                board[change[1]][change[0]]==(0,0)
            else:
                print "je n'ai pas compris l'ordre MAP"
        global nous
        nous = board[home[1]][home[0]][0]  #enregistre 'v' ou 'w' dans la variable nous
        print nous
        pprint(board)
        print "#################### fin du MAP ###################"
        print "\n\n"



    elif order == "END":
        #ici on met fin a la partie en cours Reinitialisez votre modele
        break



    elif order == "BYE":
        break



    else:
        print("commande non attendue recue", order)

#Preparez ici la deconnexion
                


#Fermeture de la socket
sock.close()