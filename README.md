ECP_IA
======

Projet pour le cours d'IA. Vampires vs Werewolves

Informations
------------
Ne pas fixer de maximum pour la carte ou le nombre de personnage. 
L'an dernier les max étaient de l'ordre de : carte 30*15 et centaine de personnages


ToDo
----

* prevenir les boucles

* reprendre heuristic step by step et incrémenter au fur et à mesure le nombre d'input

* smart_next_move = regarde les alternatives de next move 
		qui ne ralongent pas le chemin 
		et qui peuvent manger des humains au plus aussi nombreux que nous
		ou des ennemis qui sont au plus 2/3 de fois notre nombre
		et qui evitent de se mettre adjacents à des ennemis au moins aussi nombreux que nous

* faire en sorte de ne choisir que des alternatives qui ont des objectifs différents

* élaguer les triplets d'alternatives considérées