board = {}
home = ()  #stock le tuple de coodonnees de notre maison. variable qui servira a identifier si on est des v ou des w
nous = ''  #variable qui contiendra 'v' si on est des v ou 'w' si on est des w
eux = ''  #variable qui contiendra 'w' si on est des v ou 'v' si on est des w
nous_fixe = ''
eux_fixe = ''
Xsize = 0
Ysize = 0
cst_heuri = 0
#address = ("127.0.0.1",5555)
nb_of_h_positions_at_start = 0
dominance= 0   # variable needed to know wich sound to play at the end of the game
best_move = []
timer_ok = True
#ai_linear = False
ai_linear = True
address = ''