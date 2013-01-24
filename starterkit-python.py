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
groupname = "1" #mettez ici le nom de votre equipe
send(sock, "NME", len(groupname), groupname)

#boucle principale
while True:
    order = sock.recv(3)
    print order
    if not data:
        print("Bizarre, c'est vide")

    if order == "SET":
        lignes, colonnes = (struct.unpack('=B', sock.recv(1))[0] for i in range(2))
        #ici faire ce qu'il faut pour preparer votre representation de la carte
        board = [[0]*lignes]*colonnes
    elif order == "HUM":
        n = struct.unpack('=B', sock.recv(1))[0]
        maisons = []
        for i in range(n):
            maisons.append((struct.unpack('=B', sock.recv(1))[0] for i in range(2)))
        #maisons contient la liste des coordonnees des maisons
        #ajoutez votre code ici
    elif order == "HME":
        x, y = (struct.unpack('=B', sock.recv(1))[0] for i in range(2))
        #ajoutez le code ici (x,y) etant les coordonnees de votre
        #maison
    elif order == "UPD":
        n = struct.unpack('=B', sock.recv(1))[0]
        changes = []
        for i in range(n):
            changes.append((struct.unpack('=B', sock.recv(1))[0] for i in range(5)))
        #mettez a jour votre carte a partir des tuples contenus dans changes
        #calculez votre coup
        #preparez la trame MOV ou ATK
        #Par exemple:
        send(sock, "MOV", 1,2,1,1,3)
    elif order == "MAP":
        n = struct.unpack('=B', sock.recv(1))[0]
        changes = []
        for i in range(n):
            changes.append((struct.unpack('=B', sock.recv(1))[0] for i in range(n)))
        #initialisez votre carte a partir des tuples contenus dans changes
    elif order == "END":
        #ici on met fin a la partie en cours
        #Reinitialisez votre modele
        break
    elif order == "BYE":
        break
    else:
        print("commande non attendue recue", order)

#Preparez ici la deconnexion
                
#Fermeture de la socket
    sock.close()






