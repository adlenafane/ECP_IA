import config
from ai import Stuxnet

class Conductor():
	""" 
		This class performs the computation of the tree and output the good move
	"""
	def __init__(self, our_ia = Stuxnet(), other_ia = Stuxnet()):
		self.our_ia = our_ia
		self.other_ia = other_ia
		self.best_order = []
		self.best_value = []

	def minmax(self, player, current_move, max_level = 5):
		'''
			Use the minmax algorithm to compute the smartest move!
			player = 1 if we are playing and -1 for the other
		'''
		current_board = current_move[0]
		print "max_level", max_level
		if max_level == 0:
			# Score, move, needed_depth
			return (current_board.score(), None, 0)

		print "current_move", current_move
		print "current_board", current_board
		current_score = current_board.score()

		print 'current_score', current_score
		if abs(current_score) == config.cst_heuri:
			# Score, move, needed_depth
			return current_score, None, 0

		# Next move should have the following format [Board, Order]
		next_moves = []

		# Get the next moves
		if  player == 1:
			next_moves = self.our_ia.find_smart_move()
			print "next_moves", next_moves
		else:
			next_moves = self.other_ia.find_smart_move()
			print "next_moves", next_moves

		# Initialize the variables
		best_score = -player*float('inf')
		needed_depth = max_level-1
		best_move = None

		# Let's dig!
		for move in next_moves:
			current_score, current_move, current_depth = self.minmax(-player, move, needed_depth)
			print 'minmax-score', current_score
			print 'minmax-move', current_move
			print 'minmax-depth', current_depth
			if max_level == 4:
				print "Score for column %s: %s"%(current_move, current_score)
			if (player==-1 and current_score<best_score) or (player==1 and current_score>best_score) or (current_score==best_score and current_depth<=needed_depth):
				best_move = move
				best_score = current_score
				if best_score*player == config.cst_heuri:
					needed_depth = current_depth

		if best_move == None:
			return [current_board.score(), None, 0]
		return best_score, best_move, needed_depth+1