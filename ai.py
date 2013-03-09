from utility import findNextMove, Board, computeMinDistance
import config
import copy
import pprint
from operator import itemgetter

class Stuxnet():
	""" Class to handle our AI"""
	def __init__(self, mission_list = ['attack'], game_graph = [], stack_to_evaluate = []):
		print "Stuxnet::__init__"
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
		print "Stuxnet::update_game_graph"

		self.game_graph = [board]
	
	def find_smart_move(self):
		'''
			Called once in the main loop and return the smartest order we could find
			Implementation of the min/max or alpha/beta :)
			For now we make only one round (just find_best_moves actually)
		'''
		print "Stuxnet::find_smart_move"

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
		pprint.pprint(best_order)
		best_order = sorted(best_order, key=itemgetter(2), reverse=True)
		pprint.pprint(best_order)
		next_order = self.select_best_move(best_order)
		return next_order

	def find_best_moves(self, current_board):
		'''
			From a given board, evaluate all the missions in mission list
			And for all the mission, generate all the outputs for this mission and make a first clean
		'''
		print "Stuxnet::find_best_moves"
		# Receiver for all the alternatives we may find
		all_positions = []
		all_positions.extend(current_board.our_positions())
		all_positions.extend(current_board.human_positions())
		all_positions.extend(current_board.ennemy_positions())
		alternatives = []


		# Let's go throught all possibilites !
		for our_position in current_board.our_positions():
			for other_position in all_positions:
				# Let's consider the distincts cases
				if other_position.coord != our_position.coord:
					for mission in self.mission_list:
						# We should not try not attack our_positions
						if self.is_mission_compliant(other_position.kind, mission):
							target_board, next_order = self.compute_mission_result(current_board, mission, our_position, other_position)
							mission_score = float(target_board.score()/computeMinDistance(our_position.coord, other_position.coord))
							print "mission_score", our_position.coord, other_position.coord
							print "target_board.score", target_board.score()
							print "Distancce", computeMinDistance(our_position.coord, other_position.coord)
							alternatives.append((target_board, next_order, mission_score))

		# Sort the list based on the score
		alternatives = sorted(alternatives, key=itemgetter(2), reverse=True)
		order = self.generate_move(alternatives)
		return order

	def is_mission_compliant(self, other_position_kind, mission):
		'''
			From the kind of the other position evaluate if the mission makes sense
			For instance 'e', attack will return True but 'o', attack will return False
		'''
		print "Stuxnet::is_mission_compliant"
		return True

	def compute_mission_result(self, current_board, mission, our_position, other_position):
		'''
			From the current board, the mission and the 2 considered elements compute the targeted board and the next order
		'''
		print "Stuxnet::compute_mission_result"
		new_board = copy.deepcopy(current_board)
		next_order = []

		if mission == 'attack':
			# Remove our position from the board, format of our_position ('coordonees', 'nombre')
			del new_board.grid[our_position.coord]

			# Remove their position from the board, format of other_position ('kind', 'coordonees', 'nombre')
			del new_board.grid[other_position.coord]

			# Add our team on the ennemy position
			if other_position.kind == 'h':
				new_board.grid[other_position.coord] = (our_position.kind, our_position.number + other_position.number)
				# Send the same number of human is enough
				number_needed = int(other_position.number)
			elif other_position.kind == config.eux:
				# Use the probability given by the pdf to compute the estimate survivors
				new_board.grid[other_position.coord] = (our_position.kind, float(2*our_position.number/3*other_position.number))
				# We should send at least 1.5 time the number of ennemies
				number_needed = int(1.5 * other_position.number) + 1
			elif other_position.kind == config.nous:
				new_board.grid[other_position.coord] = (our_position.kind, our_position.number + other_position.number)
				number_needed = our_position.number
			else:
				number_needed = 0
				print "That should not happens :/"
			
			number_sent = min(number_needed, our_position.number)
			nextCoord = findNextMove(our_position.coord, other_position.coord)
			next_order = ['MOV', 1, our_position.coord[0], our_position.coord[1], number_sent, nextCoord[0], nextCoord[1]]
		else:
			pass
		
		return new_board, next_order

	def select_best_move(self, best_order):
		'''
			Once we have computed all the possible move, select the best one
		'''
		print "Stuxnet::select_best_move"
		return best_order[0]

	def generate_move(self, alternatives):
		'''
			From a list of alternatives (e.g. possible orders), find the best compliant one:
			Check to have:
			- Do not use too many people
			- Do not make moves from the same position
			- Do not send more than 1 attack or 3 moves
			- Do not ask to go out of the board
		'''
		return alternatives

def main():
	"""
    to run the tests
    this part is executed only when the file is executed in command line 
    (ie not executed when imported in another file)
    """
	grid = {(0,0):('h',5),(2,5):('v',4),(1,4):('w',3),(4,3):('h',2),(5,0):('h',3),(2,2):('v',4),(4,8):('w',5),(8,8):('w',2),(5,9):('v',4)}

	config.nous = 'v'
	config.eux = 'w'

	board = Board(grid,10,10)
	stuxnet = Stuxnet()
	stuxnet.update_game_graph(board)
	pprint.pprint(stuxnet.find_smart_move())

if __name__=="__main__":
    main()