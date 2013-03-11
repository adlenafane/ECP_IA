from utility import findNextMove, Board, computeMinDistance
import config
import copy
import pprint
from operator import itemgetter


def alternatives_same_target_clean(input_alternatives):
	"""
	(target_board, next_order, mission_score,other_position.coord)
	"""
	alternatives = input_alternatives
	idx_to_del=[]

	for i in range(len(alternatives)):
		target = alternatives[i][3]
		print "alternatives[i][3]: ", target
		for j in range(i+1,len(alternatives)):
			if alternatives[j][3]==target and alternatives[j][4]!=config.nous: 
				alternatives.pop(j) #the alternative with same target and worse score of another alternative is removed from the list of alternatives if it's not a merge
				return alternatives_same_target_clean(alternatives)
	return alternatives


"""	alternatives = input_alternatives
	idx_to_del=[]

	for i in range(len(alternatives)):
		target = alternatives[i][3]
		print "alternatives[i][3]: ", target
		for j in range(i+1,len(alternatives)):
			if alternatives[j][3]==target and alternatives[j][4]!=config.nous: 
				idx_to_del.append(j) #the alternative with same target and worse score of another alternative is removed from the list of alternatives if it's not a merge
		
	for index in sorted(idx_to_del, reverse = True):  # if items were poped out during the for statement above, every time an item is poped generates an item out of range in the next iterations !
		del alternatives[index]                       # Note that you need to delete them in reverse order so that you don't throw off the subsequent indexes.

	return alternatives"""


class Stuxnet():
	""" Class to handle our AI"""
	def __init__(self, mission_list = ['attack'], game_graph = [], stack_to_evaluate = []):
		#print "\n"+"#"*50+"\nStuxnet::__init__"
		self.mission_list = mission_list
		self.game_graph =  game_graph
		self.stack_to_evaluate = stack_to_evaluate



	def update_game_graph(self, board):
		'''
			Generate the new game graph.
			For now it replaces the current game_graph with the given board
			TODO:
			- Remind the past
			- Cut only the wrong branches
		'''
		#print "\n"+"#"*50+"\nStuxnet::update_game_graph"

		self.game_graph = [board]
	


	def find_smart_move(self):
		'''
			Called once in the main loop and return the smartest order we could find
			Implementation of the min/max or alpha/beta :)
			For now we make only one round (just find_best_moves actually)
		'''
		
		# Add current element to the stack
		self.stack_to_evaluate.append(self.game_graph[0])
		while self.stack_to_evaluate != []:
			# Get the next element to evaluate
			# For the future we will probably have to implement a .pop() or similar
			current_board = self.stack_to_evaluate[0]

			'''For testing purpose, we have to "pop" the element IRL '''
			self.stack_to_evaluate = []
			# From the possibility (a board) compute the next smart possible moves
			best_order = self.find_best_moves(current_board)

			''' IRL we have to add the next elements to evaluate in the stack_to_evaluate '''
		print "\nStuxnet::find_smart_move"
		print "This is the sorted best order:"
		#best_order = sorted(best_order, key=itemgetter(2), reverse=True)
		#print "-"*50
		#print "-"*50
		#for order in best_order:
		#	print "ordre: " + str(order[1]) +", score: " + str(order[2])
		#print "-"*50
		#print "-"*50
		next_order = self.select_best_move(best_order)
		smart_order = self.smart_move_filter(next_order, current_board)
		return smart_order



	def find_best_moves(self, current_board):
		'''
			From a given board, evaluate all the missions in mission list
			And for all the mission, generate all the outputs for this mission and make a first clean
		'''
		print "\n"+"-"*120+"\nStuxnet::find_best_moves"
		# Receiver for all the alternatives we may find
		all_positions = []
		all_positions.extend(current_board.our_positions())
		all_positions.extend(current_board.human_positions())
		all_positions.extend(current_board.ennemy_positions())
		alternatives = []

		fmt="%11s%12s%10s%13s%13s%15s"
		print fmt % ('coord_start', 'coord_goal', 'distance', 'target_type', 'board_score', 'mission_score')
		# Let's go throught all possibilites !
		for our_position in current_board.our_positions():
			for other_position in all_positions:
				# Let's consider the distincts cases
				if other_position.coord != our_position.coord:
					for mission in self.mission_list:
						# We should not try not attack our_positions
						if self.is_mission_compliant(other_position.kind, mission):
							target_board, next_order, delta_our = self.compute_mission_result(current_board, mission, our_position, other_position)
							if target_board.score() > 0:
								mission_score = float(target_board.score()/(computeMinDistance(our_position.coord, other_position.coord)**2)) * delta_our
							else:
								if delta_our > 0:
									mission_score = float(target_board.score())*(computeMinDistance(our_position.coord, other_position.coord)**2)/ delta_our
								else:
									mission_score = float(target_board.score()*(computeMinDistance(our_position.coord, other_position.coord)**2))*abs(delta_our)
							print fmt % (our_position.coord, other_position.coord, computeMinDistance(our_position.coord, other_position.coord), other_position.kind, round(target_board.score(),1), round(mission_score,1))
							alternatives.append((target_board, next_order, mission_score,other_position.coord,other_position.kind))
		print "-"*120

		# Sort the list based on the score
		alternatives = sorted(alternatives, key=itemgetter(2), reverse=True)
		alternatives = alternatives_same_target_clean(alternatives)
		order = self.generate_move(alternatives, current_board)
		order_to_send = self.generate_order_format(order)
		return order_to_send



	def is_mission_compliant(self, other_position_kind, mission):
		'''
			From the kind of the other position evaluate if the mission makes sense
			For instance 'e', attack will return True but 'o', attack will return False
		'''
		#print "\n"+"#"*50+"\nStuxnet::is_mission_compliant"
		return True



	def compute_mission_result(self, current_board, mission, our_position, other_position):
		'''
			From the current board, the mission and the 2 considered elements compute the targeted board and the next order
		'''
		#print "\n"+"#"*50+"\nStuxnet::compute_mission_result"
		new_board = copy.deepcopy(current_board)
		next_order = []
		delta_our = 0.0

		if mission == 'attack':
			# Remove our position from the board
			del new_board.grid[our_position.coord]

			# Remove their position from the board
			del new_board.grid[other_position.coord]

			# Add our team on the ennemy position
			if other_position.kind == 'h':
				if our_position.number >= other_position.number:
					new_board.grid[other_position.coord] = (our_position.kind, our_position.number + other_position.number)
					delta_our = float(other_position.number)
				else:
					# We will die
					new_board.grid[other_position.coord] = (other_position.kind, other_position.number)
					delta_our = float(-our_position.number)
				# Send the same number of human is enough
				number_needed = int(other_position.number)
			elif other_position.kind == config.eux:
				if our_position.number >= other_position.number:
					if our_position.number >= int(1.5 * other_position.number) + 1:
						# Use the probability given by the pdf to compute the estimate survivors
						new_board.grid[other_position.coord] = (our_position.kind, our_position.number)
						delta_our = 1.0
					else:
						new_board.grid[other_position.coord] = (our_position.kind, float((2.0/3)*our_position.number))
						delta_our = float((1.0/3)*our_position.number)
				else:
					if other_position.number >= 1.5 * our_position.number:
						new_board.grid[other_position.coord] = (other_position.kind, other_position.number)
						delta_our = float(-our_position.number)
					else:
						new_board.grid[other_position.coord] = (other_position.kind, float(other_position.number - (2.0/3)*our_position.number))
						delta_our = float(-our_position.number)
				# We should send at least 1.5 time the number of ennemies
				number_needed = int(1.5 * other_position.number) + 1
			elif other_position.kind == config.nous:
				new_board.grid[other_position.coord] = (our_position.kind, our_position.number + other_position.number)
				number_needed = our_position.number
				delta_our = 0.0
			else:
				number_needed = 0
				print "That should not happen :/"
			
			number_sent = min(number_needed, our_position.number)
			nextCoord = findNextMove(our_position.coord, other_position.coord)
			next_order = ['MOV', 1, our_position.coord[0], our_position.coord[1], number_sent, nextCoord[0], nextCoord[1]]
		else:
			pass
		
		return new_board, next_order, delta_our



	def select_best_move(self, best_order):
		'''
			Once we have computed all the possible move, select the best one
		'''
		#print "\n"+"#"*50+"\nStuxnet::select_best_move"
		return best_order



	def generate_move(self, alternatives, current_board):
		'''
			From a list of alternatives (e.g. possible orders), find the best compliant one:
		'''
		#print "\n"+"#"*50+"\nStuxnet::generate_move"
		#move_is_valid = False
		order = self.smart_three_in_n(alternatives, current_board)
		#move_is_valid = self.is_order_valid(order, current_board)
		return order



	def is_order_valid(self, orders, current_board):
		'''
			 Check if a given order is valid
		 	- Do not use too many people
			- Do not make moves from the same position
			- Do not send more than 1 attack or 3 moves
			- Do not ask to go out of the board
		''' 

		# Order length
		if len(orders) > 3:
			print "\n"+"#"*50+"\nStuxnet::is_order_valid"+"\nOrder is too long (weird)"
			return False

		# Check if count is ok
		move_count = {}
		for order_full in orders:
			# Order full is (Board, order, score)
			order = order_full[1]
			coord_start = (order[2], order[3])
			try:
				value = move_count[coord_start]
			except:
				value = -1
			if value !=-1:
				move_count[coord_start]+=order[4]
			else:
				move_count[coord_start] = order[4]
		print "move_count", move_count
		for k in move_count.keys():
			print "current_board.grid[k]", current_board.grid[k][1]
			if move_count[k] > current_board.grid[k][1]:
				print "\n"+"#"*50+"\nStuxnet::is_order_valid"+"\nInvalid split", k
				return False

		# Valid position and attack count
		attack_count = 0
		for order_full_1 in orders:
			order_1 = order_full_1[1]
			if order_1[0] == 'ATK':
				attack_count+=1
			if order_1[5] < 0 or order_1[6] < 0 or order_1[5]>config.Xsize or order_1[6]>config.Ysize:
				print "\n"+"#"*50+"\nStuxnet::is_order_valid"+"\nOrder asks to go out of the board: ", order_1
				return False
			# Check if move is valid
			for order_full_2 in orders:
				order_2 = order_full_2[1]
				if order_1[5] == order_2[2] and order_1[6] == order_2[3]:
					print "\n"+"#"*50+"\nStuxnet::is_order_valid"+"\nInvalid way to move our troops: "
					print "order_1", order_1
					print "order_2", order_2
					return False

		if attack_count > 1:
			print "\n"+"#"*50+"\nStuxnet::is_order_valid"+"\nToo many attacks asked"
			return False

		#print "\n"+"#"*50+"\nStuxnet::is_order_valid"+"\nCongrats, order seems to be valid!"
		return True



	def smart_three_in_n(self, alternatives, current_board):
		'''
			Implementation of the function described by Edouard
		'''
		#print "\n"+"#"*50+"\nStuxnet::smart_three_in_n"
		alternatives = alternatives[:10]
		for alternative_1 in alternatives:
			print "alternative_1", alternative_1
			for alternative_2 in alternatives:
				if alternative_2 != alternative_1:
					print "alternative_2", alternative_2
					if self.is_order_valid([alternative_1, alternative_2], current_board):
						for alternative_3 in alternatives:
							print "alternative_3", alternative_3
							if alternative_2 != alternative_3 and alternative_3 != alternative_1:
								if self.is_order_valid([alternative_1, alternative_2, alternative_3], current_board):
									return [alternative_1, alternative_2, alternative_3]
						return [alternative_1, alternative_2]
		return [alternative_1]



	def generate_order_format(self, alternatives):
		'''
			From the best combination of alternatives, generate the proper order
		'''
		#print "\n"+"#"*50+"\nStuxnet::generate_order_format"
		order_to_send = []
		alternative_1 = alternatives[0]
		order_to_send.extend(alternative_1[1])
		print "alternatives", alternatives

		if len(alternatives)>1:
			alternative_2 = alternatives[1]
			if alternative_1[1][2] == alternative_2[1][2] and alternative_1[1][3] == alternative_2[1][3] and alternative_1[1][5] == alternative_2[1][5] and alternative_1[1][6] == alternative_2[1][6]:
				order_to_send[4] += alternative_2[1][4]
			else:
				for i in alternative_2[1][2:]:
					order_to_send.extend([i])
			if len(alternatives) > 2:
				alternative_3 = alternatives[2]
				if alternative_1[1][2] == alternative_3[1][2] and alternative_1[1][3] == alternative_3[1][3] and alternative_1[1][5] == alternative_3[1][5] and alternative_1[1][6] == alternative_3[1][6]:
					order_to_send[4] += alternative_3[1][4]
				elif alternative_2[1][2] == alternative_3[1][2] and alternative_2[1][3] == alternative_3[1][3] and alternative_2[1][5] == alternative_3[1][5] and alternative_2[1][6] == alternative_3[1][6]:
					order_to_send[9] += alternative_3[1][4]
				else:
					for i in alternative_3[1][2:]:
						order_to_send.extend([i])
		if len(order_to_send) == 7:
			order_to_send[1] = 1
		elif len(order_to_send) == 12:
			order_to_send[1] = 2
		elif len(order_to_send) == 17:
			order_to_send[1] = 3
		else:
			print "That should not happen :/"
		print "order_to_send", order_to_send
		return order_to_send



	def smart_move_filter(self, mov, current_board):
		"""
		according to the mov order, make departing cells empty to avoid letting small groups lagging behind...
		reminder: syntax of a mov order: ['MOV', 1, our_position.coord[0], our_position.coord[1], number_sent, nextCoord[0], nextCoord[1]]
		"""

		#number of orders:
		n = mov[1]
		print 'mov', mov
		#initialize new_mov:
		new_mov=copy.deepcopy(mov)

		#fetch departure coordinates
		start_coords=[] #list of departure tuples [(x,y),...]
		for i in range(n):
			start_coords.append((mov[2+5*i],mov[3+5*i]))
		print "start_coords", start_coords
		if n==1:
			new_mov[4]=current_board.grid[start_coords[0]][1]

		if n==2:
			if start_coords[0]==start_coords[1]:
				new_mov[4]=current_board.grid[start_coords[0]][1]-mov[9] #creature number on the board minus number needed for mission 2
			else:
				new_mov[4]=current_board.grid[start_coords[0]][1]
				new_mov[9]=current_board.grid[start_coords[1]][1]

		if n==3:
			if start_coords[0]==start_coords[1] and start_coords[0]==start_coords[2]:
				new_mov[4]=current_board.grid[start_coords[0]][1]-mov[9]-mov[14]
			elif start_coords[0]==start_coords[1]:
				new_mov[4]=current_board.grid[start_coords[0]][1]-mov[9]
			elif start_coords[0]==start_coords[2]:
				new_mov[4]=current_board.grid[start_coords[0]][1]-mov[14]
			elif start_coords[1]==start_coords[2]:
				new_mov[9]=current_board.grid[start_coords[1]][1]-mov[14]
			else:
				new_mov[4]=current_board.grid[start_coords[0]][1]
				new_mov[9]=current_board.grid[start_coords[1]][1]				
				new_mov[14]=current_board.grid[start_coords[2]][1]				

		return new_mov




def main():
	"""
    to run the tests
    this part is executed only when the file is executed in command line 
    (ie not executed when imported in another file)
    """
	grid = {(0,0):('h',5),(2,5):('v',4),(1,4):('w',3),(4,3):('h',2),(5,0):('h',3),(2,2):('v',4)}
	"""
		0 	1 	2 	3 	4 	5
	0	h5					h3
	1 						
	2 			v4				
	3 					h2			
	4 		w3					
	5 			v4					
	"""


	config.nous = 'v'
	config.eux = 'w'

	board = Board(grid,10,10)
	stuxnet = Stuxnet()
	#stuxnet.update_game_graph(board)
	#pprint.pprint(stuxnet.find_smart_move())
	print "test mov 1"
	print stuxnet.smart_move_filter(['MOV', 1, 2,2,1,3,2], board)
	print "\n"

	print "test mov 2"
	print stuxnet.smart_move_filter(['MOV', 2, 2,2,1,3,2,2,2,1,2,3], board)
	print "\n"



if __name__=="__main__":
    main()