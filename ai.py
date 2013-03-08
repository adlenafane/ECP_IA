from utility import Board, VectorPosition
import copy

class Stuxnet():
	""" Class to handle our AI"""
	def __init__(self, arg):
		self.mission_list = ['attack']
		self.game_graph = []
		self.stack_to_evaluate = []

	def update_game_graph(self, board):
		'''
			Generate the new game graph.
			For now it replaces the current game_graph with the given board
			TODO:
			- Remind the past
			- Cut only the wrong branches
		'''
		self.game_graph = [board]
	
	def find_smart_move(self):
		'''
			Called once in the main loop and return the smartest order we could find
			Implementation of the min/max or alpha/beta :)
			For now we make only one round (just find_best_moves actually)
		'''
		# Add current element to the stack
		self.stack_to_evaluate = self.game_graph[0]
		while self.stack_to_evaluate != []:
			# Get the next element to evaluate
			# For the future we will probably have to implement a .pop() or similar
			current_board = self.stack_to_evaluate[0]

			'''For testing purpose, we have to "pop" the element IRL '''
			self.stack_to_evaluate = []
			# From the possibility (a board) compute the next smart possible moves
			best_moves = self.find_best_moves(current_board)

			''' IRL we have to add the next elements to evaluate in the stack_to_evaluate '''
		next_order = self.select_best_move(best_moves)
		return next_order

	def find_best_moves(self, current_board):
		'''
			From a given board, evaluate all the missions in mission list
			And for all the mission, generate all the outputs for this mission and make a first clean
		'''
		# Concatene all positions (we may want to attack ennemies and humans and we may want to join our friends)
		all_positions = current_board.our_positions() + current_board.ennemy_positions() + current_board.human_positions()

		# Receiver for all the alternatives we may find
		alternatives = []

		# Let's go throught all possibilites !
		for our_position in current_board.our_position():
			for other_position in all_positions:
				# Let's consider the distincts cases
				if other_position != our_position:
					for mission in self.mission_list:
						# We should not try not attack our_positions
						if self.is_mission_compliant(other_position.kind(), mission):
							target_board, next_order = self.compute_mission_result(current_board, mission, our_position, other_position)
							missionScore = self.computeMissionScore(mission, current_board, target_board)
							alternatives.append((target_board, next_order, missionScore))
		# Sort the list based on the score
		# moves = alternatives.sort()

		moves = []

		best_moves = self.cleanMoves(moves)
		return best_moves

	def is_mission_compliant(self, other_position_kind, mission):
		'''
			From the kind of the other position evaluate if the mission makes sense
			For instance 'e', attack will return True but 'o', attack will return False
		'''
		return True

	def compute_mission_result(self, current_board, mission, our_position, other_position):
		'''
			From the current board, the mission and the 2 considered elements compute the targeted board and the next order
		'''
		new_board = copy.deepcopy(current_board)
		next_order = []

		if mission == 'attack':
			# Remove our position from the board, format of our_position ('coordonees', 'nombre')
			del new_board.grid[our_position.coord()]
			# Remove their position from the board, format of other_position ('kind', 'coordonees', 'nombre')
			del new_board.grid[other_position.coord()]
			# Add our team on the ennemy position
			if other_position.kind() == 'h':
				new_board.grid[other_position.coord()] = (our_position.kind(), our_position.number() + other_position.number())
			else:
				new_board.grid[other_position.coord()] = (our_position.kind(), our_position.number())
			nextCoord = findNextMove(our_position.coord(), other_position.coord())
			next_order = ['MOV', 1, our_position.coord()[0], our_position.coord()[1], our_position.number(), nextCoord[0], nextCoord[1]]
		else:
			pass
		
		return new_board, next_order

	def computeMissionScore(self, mission, current_board, target_board):
		'''
			Compute the score of a given mission, based on the heuristic function 
		'''
		return 0

	def cleanMoves(self, moves):
		'''
			From a list of moves, keeps only the best ones (TOP 5 or only those with a given score...)
		'''
		best_moves = []
		return best_moves

	def select_best_move(self, best_moves):
		'''
			Once we have computed all the possible move, select the best one
		'''
		next_order = []
		return next_order