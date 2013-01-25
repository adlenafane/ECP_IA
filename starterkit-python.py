# -*- coding: utf-8 -*-
import socket, struct

data = []
def send(sock, *messages):
    """Send a given set of messages to the server."""
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
"""#Creation de la socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connexion de la socket
try:
    sock.connect(("127.0.0.1", 5555)) #Changez ici l'adresse ip et le port
except Exception as error:
    print("Connection error: ", error)
"""
client = Client()
sock = client.s

#Envoi du nom
groupname = "les gerriers" #mettez ici le nom de votre equipe
send(sock, "NME", len(groupname), groupname)
print "hello"
print data

#boucle principale
while True:
    order = sock.recv(3)
    print order
    if not data:
        print("Bizarre, c'est vide")

    if order == "SET":
        lignes, colonnes = (struct.unpack('=B', sock.recv(1))[0] for i in range(2))   #B est le format pour unsigned char donc sock.recv(1) permet de lire 1 entier. The result of struct.unpack(format, string) is a tuple even if it contains exactly one item. l'opération est faite 2 fois pour récupérer ligne et colonne.
        #ici faire ce qu'il faut pour preparer votre representation de la carte
        board = [[0]*lignes]*colonnes
        print board
            #0: cases vides
            #1: maison (de n'importe quel type)
            #2: notre HME
            #(type,n): case occupée par npersonnages de type:(0 pour les humains, 1 pour nous, 2 pour les ennemis) de joueurs




    elif order == "HUM":
        print "on entre dans le if order == HUM"
        n = struct.unpack('=B', sock.recv(1))[0]
        print n
        maisons = []
        for i in range(n):
            x,y=(struct.unpack('=B', sock.recv(1))[0] for i in range(2)) #on génere la liste de tuples de coordonnées des maisons (humains)
            print x,y
            maisons.append((x,y)) #on génere la liste de tuples de coordonnées
        print maisons
        #maisons contient la liste des coordonnees des maisons ajoutez votre code ici
        for maison in maisons:
            board[maison[0]][maison[1]]=1
        print board



    elif order == "HME":
        x, y = (struct.unpack('=B', sock.recv(1))[0] for i in range(2))
        #ajoutez le code ici (x,y) etant les coordonnees de votre maison
        board[x][y]=2



    elif order == "UPD":
        n = struct.unpack('=B', sock.recv(1))[0]
        changes = []
        for i in range(n):
            x,y,humanNB,vampNB,wwNB = (struct.unpack('=B', sock.recv(1))[0] for i in range(5))
            changes.append((x,y,humanNB,vampNB,wwNB))
        #initialisez votre carte a partir des tuples contenus dans changes
        for change in changes:
            if change[2]!=0:
                board[change[0]][change[1]]=(0, change[2])
            elif change[3]!=0:
                board[change[0]][change[1]]=(0, change[3])
            elif change[4]!=0:
                board[change[0]][change[1]]=(0, change[4])
            elif (change[2]==0 and change[3]==0 and change[4]==0):
                board[change[0]][change[1]]=0
            else:
                print "je n'ai pas compris l'ordre UPD"
            print board

        #calculez votre coup
        #calculcoup(board)


        #preparez la trame MOV ou ATK
        #Par exemple: un ordre MOV qui fonctionne mais "ne respecte pas les regles" (je sais pas pk)
        #send(sock, "MOV", 2,5,4,2,4,4,5,4,1,5,3) #arg: "MOV" est suivi du nombre de quintuplets de deplacement n, puis des n quintuplets: (Xdepart, Ydepart, nb de pers a deplacer, X arrivee, Y arrivee)
        
        #un ex d'ordre ATK qui fonctionne:
        send(sock, "ATK",4,4)


    elif order == "MAP":
        n = struct.unpack('=B', sock.recv(1))[0]
        changes = []
        for i in range(n):
            x,y,humanNB,vampNB,wwNB = (struct.unpack('=B', sock.recv(1))[0] for i in range(5))
            changes.append((x,y,humanNB,vampNB,wwNB))
        #initialisez votre carte a partir des tuples contenus dans changes
        for change in changes:
            if change[2]!=0:
                board[change[0]][change[1]]=(0, change[2])
            elif change[3]!=0:
                board[change[0]][change[1]]=(0, change[3])
            elif change[4]!=0:
                board[change[0]][change[1]]=(0, change[4])
            elif (change[2]==0 and change[3]==0 and change[4]==0):
                board[change[0]][change[1]]=0
            else:
                print "je n'ai pas compris l'ordre MAP"
            print board


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






