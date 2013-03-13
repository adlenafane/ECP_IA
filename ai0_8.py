from utility import findNextMove, Board, computeMinDistance, VectorPosition
import config
import copy
from operator import itemgetter


class Stuxnet():
	""" Class to handle our AI"""
	def __init__(self, our_kind = '', other_kind = '', mission_list = ['attack','escape'], game_graph = []):
		#print "\n"+"#"*50+"\nStuxnet::__init__"
		self.mission_list = mission_list
		self.game_graph =  game_graph
		self.branch_number = 3
		self.our_kind = our_kind
		self.other_kind = other_kind


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
		config.nous = self.our_kind
		config.eux = self.other_kind
		current_board = self.game_graph[0]

		# Next orders [[order_to_send, target_board],[order, target_board],...]
		next_orders = self.find_best_moves(current_board)
		print "find_smart_move - current_board", current_board
		print "find_smart_move - next_orders", next_orders
		smart_results = []
		for next_order in next_orders:
			smart_order = self.smart_move_filter(next_order[0], current_board)
			smart_results.append([next_order[1], smart_order])
		# [[target_board, order_to_send],[target_board, order_to_send],...]
		return smart_results



	def find_best_moves(self, current_board):
		'''
			From a given board, evaluate all the missions in mission list
			And for all the mission, generate all the outputs for this mission and make a first clean
		'''
		print "\n"+"-"*120+"\nStuxnet::find_best_moves"
		# Receiver for all the alternatives we may find
		all_positions = []
		print 'find_best_moves - current_board', current_board
		all_positions.extend(current_board.our_positions())
		all_positions.extend(current_board.human_positions())
		all_positions.extend(current_board.ennemy_positions())
		alternatives = []

		fmt="%11s%12s%10s%13s%13s%15s%14s"
		print fmt % ('coord_start', 'coord_goal', 'distance', 'target_type', 'board_score', 'mission_score', 'mission_type')
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
							print fmt % (our_position.coord, other_position.coord, computeMinDistance(our_position.coord, other_position.coord), other_position.kind, round(target_board.score(),1), round(mission_score,1),mission)
							alternatives.append((target_board, next_order, mission_score,other_position.coord,other_position.kind))
		print "-"*120

		# Sort the list based on the score
		alternatives = sorted(alternatives, key=itemgetter(2), reverse=True)
		alternatives = self.alternatives_same_target_clean(alternatives)
		orders = self.generate_move(alternatives, current_board)
		print 'find_best_moves - orders', orders
		result = []
		for order in orders:
			order_to_send = self.generate_order_format(order)
			target_board = self.generate_target_board(order, current_board)
			result.append([order_to_send, target_board])
			print 'find_best_moves - order_to_send', order_to_send
			print 'find_best_moves - target_board', target_board
		return result



	def is_mission_compliant(self, other_position_kind, mission):
		'''
			From the kind of the other position evaluate if the mission makes sense
			For instance 'e', attack will return True but 'o', attack will return False
		'''
		if mission == 'escape' and other_position_kind != self.other_kind :
			return False
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
			elif other_position.kind == self.other_kind:
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

			elif other_position.kind == self.our_kind:
				new_board.grid[other_position.coord] = (our_position.kind, our_position.number + other_position.number)
				number_needed = our_position.number
				if other_position.number > our_position.number:
					delta_our = max(min(float(3*config.nb_of_h_positions_at_start/(current_board.x_max * current_board.y_max)),1),0) # test needed
				else:
					delta_our = 0.0

			else:
				number_needed = 0
				print "'number_needed = 0' -> That should not happen :/"
			
			number_sent = min(number_needed, our_position.number)
			next_coord = findNextMove(our_position.coord, other_position.coord)
			if computeMinDistance(our_position.coord, other_position.coord) == 1:
				next_order = ['MOV', 1, our_position.coord[0], our_position.coord[1], number_sent, next_coord[0], next_coord[1]]
			else:
				next_coord_optimized = self.optimize_next_move(current_board, our_position, other_position, next_coord)
				next_order = ['MOV', 1, our_position.coord[0], our_position.coord[1], number_sent, next_coord_optimized[0], next_coord_optimized[1]]
		
		

		elif mission == 'escape' : # maybe add 'and self.our_number() > ennemies around' 
			# Remove our position from the board
			del new_board.grid[our_position.coord]

			# Compute the 8 possible positions minus out-of-board positions
			escape_scope = {}
			x_range=[i for i in range(config.Xsize)]
			y_range=[i for i in range(config.Ysize)]
			if (our_position.x-1) in x_range and (our_position.y-1) in y_range : escape_scope[(our_position.x-1,our_position.y-1)] = []
			if (our_position.x) in x_range and (our_position.y-1) in y_range : escape_scope[(our_position.x,our_position.y-1)]= []
			if (our_position.x+1) in x_range and (our_position.y-1) in y_range : escape_scope[(our_position.x+1,our_position.y-1)]= []
			if (our_position.x+1) in x_range and (our_position.y) in y_range : escape_scope[(our_position.x+1,our_position.y)]= []
			if (our_position.x+1) in x_range and (our_position.y+1) in y_range : escape_scope[(our_position.x+1,our_position.y+1)]= []
			if (our_position.x) in x_range and (our_position.y+1) in y_range : escape_scope[(our_position.x,our_position.y+1)]= []
			if (our_position.x-1) in x_range and (our_position.y+1) in y_range : escape_scope[(our_position.x-1,our_position.y+1)]= []
			if (our_position.x-1) in x_range and (our_position.y) in y_range : escape_scope[(our_position.x-1,our_position.y)]= []

			# add distance to ennemy 
			for position in escape_scope.keys():
				escape_scope[position].append(computeMinDistance(position, other_position.coord))

			# create list of friends' positions
			our_other_positions=[position.coord for position in current_board.our_positions()]
			#print our_other_positions
			our_other_positions.remove(our_position.coord)
			#print our_other_positions

			# determine distance to closest friend and add it to escape scope
			for position in escape_scope.keys():
				dist = float('inf')
				for our_other_position in our_other_positions:
					if computeMinDistance(position,our_other_position) < dist:
						dist = computeMinDistance(position,our_other_position)
				escape_scope[position].append(100.0/(1+dist)) #to sort in te right order, see below

			# Compute escape position by sorting escape_scope by ennemy_distance and then by friend_distance (dic is flattened in the process) -> the escape coord selected is the furthest from the ennemy, the closest from a friend
			escape_coord = sorted(([k]+v for k,v in escape_scope.iteritems()), key=itemgetter(1,2), reverse=True)[0][0] 
			# sorted -> [(x,y),ennemy_distance, friend_distance] sorted by ennemy_distance and then by 100/(1+friend_distance), from biggest to smallest

			# Add our team on the escape position on new_board
			new_board.grid[escape_coord] = (our_position.kind, our_position.number)

			# set next order:
			next_order = ['MOV', 1, our_position.coord[0], our_position.coord[1], our_position.number, escape_coord[0], escape_coord[1]]
			print "generated escape_coord", escape_coord
			print "ennemy position: ", other_position.coord
			# set delta_our

			if other_position.kind == config.eux:
				delta_our = 1.0  #to be checked !!!!!!!!!!!
			else:
				delta_our = 0.0

		else:
			pass
		
		return new_board, next_order, delta_our



	def select_best_move(self, best_order):
		'''
			Once we have computed all the possible move, select the best one
		'''
		#print "\n"+"#"*50+"\nStuxnet::select_best_move"
		return best_order



	def generate_move(self, alternatives_entry, current_board):
		'''
			From a list of alternatives (e.g. possible orders), find the best compliant branches
			Return array of orders
		'''
		#print "\n"+"#"*50+"\nStuxnet::generate_move"
		#move_is_valid = False

		# Just keep the alternatives with the highest score
		alternatives = alternatives_entry[:10]
		coord_considered = []
		for alternative in alternatives:
			if (alternative[1][2], alternative[1][3]) in coord_considered:
				pass
			else:
				coord_considered.append((alternative[1][2], alternative[1][3]))

		# Be sure to have an alternative for each one of our group
		for our_position in current_board.our_positions():
			if our_position.coord in coord_considered:
				pass
			else:				
				for alternative in alternatives_entry[10:]:
					if our_position.coord == (alternative[1][2], alternative[1][3]):
						coord_considered.append((alternative[1][2], alternative[1][3]))
						alternatives.append(alternative)
		print "alternatives all coord there?", alternatives
		
		orders = []
		for i in range(self.branch_number):
			try:
				order = self.smart_three_in_n(alternatives, current_board, i)
				if order == []:
					break
				else:
					orders.append(order)
			except:
				pass
		#move_is_valid = self.is_order_valid(order, current_board)
		return orders



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



	def smart_three_in_n(self, alternatives, current_board, branch_number):
		'''
			Implementation of the function described by Edouard
		'''
		#print "\n"+"#"*50+"\nStuxnet::smart_three_in_n"
		alternative_1 = alternatives[branch_number]
		#print "alternative_1", alternative_1
		if self.is_order_valid([alternative_1], current_board):
			for alternative_2 in alternatives:
				if alternative_2 != alternative_1:
					#print "alternative_2", alternative_2
					if self.is_order_valid([alternative_1, alternative_2], current_board):
						for alternative_3 in alternatives:
							#print "alternative_3", alternative_3
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

	def generate_target_board(self, alternatives, current_board):
		'''
			From the given alternatives, generate the target board (with the 1, 2 or 3 missions done)
		'''
		target_board = copy.deepcopy(current_board)
		
		for alternative in alternatives:
			our_coord = (alternative[1][2], alternative[1][3])
			our_kind = target_board.grid[our_coord][0]
			our_number = target_board.grid[our_coord][1]
			other_coord = alternative[3]
			other_kind = alternative[4]
			other_number = target_board.grid[other_coord][1]

			if other_kind == self.other_kind:
				if our_number >= other_number:
					if our_number >= int(1.5 * other_number) + 1:
						target_board.grid[other_coord] = (our_kind, our_number)
					else:
						target_board.grid[other_coord] = (our_kind, float((2.0/3)*our_number))
				else:
					if other_number >= 1.5 *our_number:
						target_board.grid[other_coord] = (other_kind, other_number)
					else:
						target_board.grid[other_coord] = (other_kind, float(other_number - (2.0/3)*our_number))

			elif other_kind == 'h':
				if our_number >= other_number:
					target_board.grid[other_coord] = (our_kind, our_number + other_number)
				else:
					# We will die
					target_board.grid[other_coord] = (other_kind, other_number)

			elif other_kind == self.our_kind:
				# The merge is supposed to stay on the one with the highest number (not realistic I know)
				if our_number <= other_number:
					try:
						target_board.grid[other_coord] = (our_kind, our_number + other_number)
					except:
						# If we are here it should mean that 2 groups of the same size chose to merge and we are retrying to change the position in the board
						pass
			else:
				print "That should not happen :/"

		return target_board

	def smart_move_filter(self, mov, current_board):
		"""
		according to the mov order, make departing cells empty to avoid letting small groups lagging behind...
		reminder: syntax of a mov order: ['MOV', 1, our_position.coord[0], our_position.coord[1], number_sent, nextCoord[0], nextCoord[1]]
		"""

		#number of orders:
		n = mov[1]
		#print 'mov', mov
		#initialize new_mov:
		new_mov=copy.deepcopy(mov)

		#fetch departure coordinates
		start_coords=[] #list of departure tuples [(x,y),...]
		for i in range(n):
			start_coords.append((mov[2+5*i],mov[3+5*i]))
		#print "start_coords", start_coords
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

	def optimize_next_move(self, current_board, our_position, other_position, next_coord):
		'''
			Optimize the next move by:
			- Stay away from the ennemy
			- Kill humans on our way
		'''
		#print "\n"+"#"*50+"\nStuxnet::optimize_next_move"
		best_coord = next_coord
		possible_move = self.get_possible_move(our_position, other_position)
		#print "possible_move", possible_move
		ordered_list = [[next_coord, -3]]
		for move in possible_move:
			#print "move", move
			try:
				# If there is human on this cell, we should kill them!
				if current_board.grid[move][0] == 'h' and current_board.grid[move][1]<=our_position.number:
					# However it ennemies are near and too numerous, maybe we should stay away...
					#print "human found!"
					ennemy_near = False
					for x,y in [(move[0]+i, move[1]+j) for i in (-1,0,1) for j in (-1,0,1) if i != 0 or j != 0]:
						#print "checking", x, y
						try:
							if current_board.grid[(x, y)][0] == self.other_kind and current_board.grid[(x, y)][1] >= (our_position.number + current_board.grid[move][1]):
								ennemy_near = True
								ordered_list.append([move, -1])
								#print "ennemy found and too numerous", x, y, current_board.grid[(x, y)][1]
								break
						except:
							pass
					if not ennemy_near:
						ordered_list.append([move, current_board.grid[move][1]])
			except:
				ennemy_near = False
				for x,y in [(move[0]+i, move[1]+j) for i in (-1,0,1) for j in (-1,0,1) if i != 0 or j != 0]:
					try:
						if current_board.grid[(x, y)][0] == self.other_kind and current_board.grid[(x, y)][1] >= our_position.number:
							ennemy_near = True
							ordered_list.append([move, -2])
							break
					except:
						pass
				if not ennemy_near:
					if best_coord != next_coord:
						pass
					else:
						ordered_list.append([move, 0])

		return sorted(ordered_list, key=itemgetter(1), reverse=True)[0][0]

	def get_possible_move(self, our_position, other_position):
		'''
			Return a list of the 2 or 3 possible moves
		'''
		#print "\n"+"#"*50+"\nStuxnet::get_possible_move"
		possible_move = []
		our_x = our_position.coord[0]
		our_y = our_position.coord[1]
		other_x = other_position.coord[0]
		other_y = other_position.coord[1]
		# Same column
		if our_x == other_x:
			# We are above
			if our_y < other_y:
				possible_move = [(our_x-1, our_y+1), (our_x, our_y+1), (our_x+1, our_y+1)]
			# We are below
			else:
				possible_move = [(our_x-1, our_y-1), (our_x, our_y-1), (our_x+1, our_y-1)]
		# Same line
		elif our_y == other_y:
			# We are on the left
			if our_x < other_x:
				possible_move = [(our_x+1, our_y-1), (our_x+1, our_y), (our_x+1, our_y+1)]
			# We are on the right
			else:
				possible_move = [(our_x-1, our_y-1), (our_x-1, our_y), (our_x-1, our_y+1)]
		# We have to move on the diagonal
		else:
			# Ennemy is on diagonal top left / bottom right!
			if our_y-our_x == other_y-other_x:
				# Ennemy is on the left on top left
				if our_x > other_x:
					possible_move = [(our_x-1, our_y-1)]
				# Ennemy is on the right on bottom right
				else:
					possible_move = [(our_x+1, our_y+1)]
			# Ennemy is on diagonal bottom left / top right!
			elif our_y - (config.Xsize-our_x) == other_y - (config.Xsize - other_x):
				# Ennemy is on the left on bottom left
				if our_x > other_x:
					possible_move = [(our_x-1, our_y+1)]
				# Ennemy is on the right on top right
				else:
					possible_move = [(our_x+1, our_y-1)]
			# Other position is bottom left
			elif our_y-our_x < other_y-other_x:
				# Other position is bottom right
				# --> South
				if our_y - (config.Xsize-our_x) < other_y - (config.Xsize - other_x):
					# Go South South West
					if our_x > other_x:
						possible_move = [(our_x-1, our_y+1), (our_x, our_y+1)]
					# Go South South East
					else:
						possible_move = [(our_x, our_y+1), (our_x+1, our_y+1)]
				# Other position is top left
				# --> West
				else:
					# Go North West West
					if our_y > other_y:
						possible_move = [(our_x-1, our_y-1), (our_x-1, our_y)]
					# Go South West West
					else:
						possible_move = [(our_x-1, our_y), (our_x-1, our_y+1)]
			
			# Other position is top right
			else:
				# Other position is bottom right
				# --> East
				if our_y - (config.Xsize-our_x) < other_y - (config.Xsize - other_x):
					# Go North East East
					if our_y > other_y:
						possible_move = [(our_x+1, our_y-1), (our_x+1, our_y)]
					#Go South East East 
					else:
						possible_move = [(our_x+1, our_y), (our_x+1, our_y+1)]
				# Other position is top left
				# --> North
				else:
					# Go North North West
					if our_x > other_x:
						possible_move = [(our_x-1, our_y-1), (our_x, our_y-1)]
					# Go North North East
					else:
						possible_move = [(our_x, our_y-1), (our_x+1,our_y-1)]
		valid_possible_move = []
		for move in possible_move:
			print "move", move
			if move[0]>=0 and move[1]>=0 and move[0]<config.Xsize and move[1]<config.Ysize:
				valid_possible_move.append(move)
		return valid_possible_move


	def alternatives_same_target_clean(self, input_alternatives):
		"""
		(target_board, next_order, mission_score,other_position.coord)
		"""
		alternatives = input_alternatives

		for i in range(len(alternatives)):
			target = alternatives[i][3]
			print "alternatives[i][3]: ", target
			for j in range(i+1,len(alternatives)):
				if alternatives[j][3]==target and alternatives[j][4]!=self.our_kind: 
					alternatives.pop(j) #the alternative with same target and worse score of another alternative is removed from the list of alternatives if it's not a merge
					return self.alternatives_same_target_clean(alternatives)
		return alternatives

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
	config.Xsize = 100
	config.Ysize = 100

	board = Board(grid,10,10)
	stuxnet = Stuxnet('v', 'w')
	#stuxnet.update_game_graph(board)
	#pprint.pprint(stuxnet.find_smart_move())
	print "test mov 1"
	print stuxnet.smart_move_filter(['MOV', 1, 2,2,1,3,2], board)
	print "\n"

	print "test mov 2"
	print stuxnet.smart_move_filter(['MOV', 2, 2,2,1,3,2,2,2,1,2,3], board)
	print "\n"

	our_position = VectorPosition('v', (4,4), 100)
	# other_position = VectorPosition('w', (2,2), 1)
	# other_position = VectorPosition('w', (3,2), 1)
	# other_position = VectorPosition('w', (4,2), 1)
	# other_position = VectorPosition('w', (5,2), 1)
	# other_position = VectorPosition('w', (6,2), 1)
	# other_position = VectorPosition('w', (6,3), 1)
	# other_position = VectorPosition('w', (6,4), 1)
	# other_position = VectorPosition('w', (6,5), 1)
	# other_position = VectorPosition('w', (6,6), 1)
	# other_position = VectorPosition('w', (5,6), 1)
	# other_position = VectorPosition('w', (4,6), 1)
	# other_position = VectorPosition('w', (3,6), 1)
	# other_position = VectorPosition('w', (2,6), 1)
	# other_position = VectorPosition('w', (2,5), 1)
	# other_position = VectorPosition('w', (2,4), 1)
	other_position = VectorPosition('w', (2,3), 1)
	

	print 'get_possible_move', stuxnet.get_possible_move(our_position, other_position)

if __name__=="__main__":
    main()