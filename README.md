ECP_IA
======

Projet pour le cours d'IA. Vampires vs Werewolves

Informations
------------
Ne pas fixer de maximum pour la carte ou le nombre de personnage. 
L'an dernier les max étaient de l'ordre de : carte 30*15 et centaine de personnages


ToDo
----

* on garde le board en liste de liste ou on fait un dictionaire {tuple de coordonnees : (type,nombre)}

* coder une fonction getOurPositions: -> done pour la version dico !
	entree: board, nous
	retourne: liste de tuples qui nous donne nos positions
	

* getHumanNumber(board):
	entree: board
	retourne le nombre d'humains restants sur le plateau

* getEnnemyNumber(board, nous):
	entree: board, nous
	retourne le nombre d'ennemis restants sur le plateau
	

* une fonction anyEnnemyClose()
	entree: board
	retourne: un dico avec en clé: tuple de positions des ennemis qui snt adjacents à une de nos positions, et en valeur un tuple (tuples de nos positions mmenacées, nombre de nos creatures présentes sur cette case)


* une fonction anyHumanClose()
	entree: board
	retourne: un dico avec en clé: tuple de positions des humains qui snt adjacents à une de nos positions, et en valeur un tuple (tuples de nos positions mmenacées, nombre de nos creatures présentes sur cette case)


* une fonction attack:
	entree: tuple de coordonnes de la cellule a attaquer
	nb: faire un test si la cellule cible est bien une cellule a notre portee
	retourne: le send correctement formaté


* une fonction move
	entree: une liste de quintuplets
	NB: checker ue le nombre de quintuplets est < à 3
	retourne: le send correctement formaté