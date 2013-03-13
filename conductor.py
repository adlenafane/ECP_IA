import config
import Queue
from operator import itemgetter

# from utility import Board

class Conductor():
	""" 
		This class performs the computation of the tree and output the good move
	"""
	def __init__(self, our_ia, other_ia):
		self.our_ia = our_ia
		self.other_ia = other_ia
		self.best_order = []
		self.best_value = []
		self.current_level = Queue.PriorityQueue()
		self.next_level = []
		self.best_move = []

	def minmax_smart(self, player, current_board =[], current_depth = 0, current_move = []):
		'''
			Use the minmax algorithm to compute the smartest move!
			player = 1 if we are playing and -1 for the other
			current_move = [current_board, order]
		'''
		print "minmax_smart:init"
		# We start
		if self.current_level.empty() and self.next_level == [] :
			print "minmax_smart::firstIf"
			self.our_ia.update_game_graph(current_board)
			current_board.print_board()
			next_moves = self.our_ia.find_smart_move()
			print "minmax_smart - next_moves", next_moves

			# Put the new nodes we have computed in the next layer
			for move in next_moves:
				# Format should be score of the target_board, first_move to get there (move in the first layer)
				self.next_level.append((move[0].score(), move))
				print "minmax_smart - move", move
			# Let's find the best branch from what we have just generated
			self.next_level = sorted(self.next_level, key=itemgetter(0), reverse=True)
			print "minmax_smart - next_level", self.next_level
			self.best_move = self.next_level[0][1]
			# If for a weird reason, the best_move found is void, do not update the config!!
			if self.next_level[0][1] != []:
				config.best_move = self.next_level[0][1]
			else:
				print 'That should not happen :/ - Void order'
			print "conductor - best_move", self.best_move
			current_depth = current_depth+1
			self.minmax_smart(-player, current_depth)

		# Generate the current level
		if self.current_level.empty() and self.next_level != []:
			print "minmax_smart::secondIf"
			for element in self.next_level:
				self.current_level.put(element)
			self.next_level = []
			# Let's go through the current level of depth
			while not self.current_level.empty():
				current_move = self.current_level.get()[1]
				current_board = current_move[0]
				current_board.print_board()
				# Get the next moves
				next_moves = []
				if  player == 1:
					self.our_ia.update_game_graph(current_board)
					next_moves = self.our_ia.find_smart_move()
					# print "next_moves", next_moves
				else:
					self.other_ia.update_game_graph(current_board)
					next_moves = self.other_ia.find_smart_move()
					# print "next_moves", next_moves
				# Put the new nodes we have computed in the next layer
				for move in next_moves:
					# Format should be score of the target_board, first_move to get there (move in the first layer)
					if move != []:
						self.next_level.append((move[0].score(), current_move))
			# Let's find the best branch from what we have just generated
			# Priority Queue is ranked in normal order of the score
			if self.next_level != []:
				self.next_level = sorted(self.next_level, key=itemgetter(0), reverse=True)
				print "\nminmax_smart - next_level", self.next_level
				for element in self.next_level:
					print '\nPossibility 1'
					print 'score', element[0], '\n'
					element[1].print_board()
					print '\n order', element[2]

				self.best_move = self.next_level[0][1]
				# If for a weird reason, the best_move found is void, do not update the config!!
				if self.next_level[0][1] != []:
					config.best_move = self.next_level[0][1]
				else:
					print 'That should not happen :/ - Void order'
				print "conductor - best_move", self.best_move
				current_depth = current_depth+1
				self.minmax_smart(-player, current_depth)
			else:
				return config.best_move

		else:
			# We have reached the end
			return config.best_move

	def minmax(self, player, current_move, max_level = 5):
		'''
			Use the minmax algorithm to compute the smartest move!
			player = 1 if we are playing and -1 for the other
		'''
		current_board = current_move[0]
		# print "max_level", max_level
		if max_level == 0:
			# Score, move, needed_depth
			return (current_board.score(), current_move, 0)

		# print "current_move", current_move
		# print "current_board", current_board
		current_score = current_board.score()

		# print 'current_score', current_score
		if abs(current_score) == config.cst_heuri:
			# Score, move, needed_depth
			return current_score, current_move, 0

		# Next move should have the following format [Board, Order]
		next_moves = []

		# Get the next moves
		if  player == 1:
			next_moves = self.our_ia.find_smart_move()
			# print "next_moves", next_moves
		else:
			next_moves = self.other_ia.find_smart_move()
			# print "next_moves", next_moves

		# Initialize the variables
		best_score = -player*float('inf')
		needed_depth = max_level-1
		best_move = None

		# Let's dig!
		for move in next_moves:
			current_score, current_move, current_depth = self.minmax(-player, move, needed_depth)
			# print 'minmax-score', current_score
			# print 'minmax-move', current_move
			# print 'minmax-depth', current_depth
			if max_level == 4:
				print "Score for column %s: %s"%(current_move, current_score)
			if (player==-1 and current_score>best_score) or (player==1 and current_score>best_score) or (current_score==best_score and current_depth<=needed_depth):
				best_move = move
				best_score = current_score
				if best_score*player == config.cst_heuri:
					needed_depth = current_depth

		if best_move == None:
			return [current_board.score(), current_move, 0]
		return best_score, best_move, needed_depth+1

	def IDDFS(self, current_board, player = 1):
		depth = 0
		current_move = (current_board.score(), current_board, [])
		while config.timer_ok:
			move = self.alphabeta(player, current_move, depth, first_iteration=True)
			print 'IDDFS - best_move', move
			if move != []:
				config.best_move = move
			print 'IDDFS - depth', depth
			depth+=1

	def alphabeta(self, player, current_move, depth, first_iteration = False, alpha = -float('inf'), beta = float('inf')):
		'''
			move = [score, board, next_order]
			find_smart_move return [board, next_order]
		'''
		if depth == 0:
			print 'depht 0 - move', current_move
			return current_move

		# Handle our first move to have good first orders
		if first_iteration:
			print 'first_iteration'
			current_board = current_move[1]
			print 'alphabeta - first_iteration - current board', current_board
			best_moves = []
			computed_move = []
			self.our_ia.update_game_graph(current_board)
			next_moves = self.our_ia.find_smart_move()

			# print "next_moves", next_moves
			for move in next_moves:
				board = move[0]
				print 'alphabeta move', move
				computed_move = self.alphabeta(-player, (board.score(), board, move[1]), depth-1, False, alpha, beta)
				best_moves.append(computed_move)
			print 'alphabeta - best_moves - first_iteration', best_moves
			return sorted(best_moves, key=itemgetter(0), reverse=True)[0]

		# For depth > 0
		print 'alphabeta - current move', current_move
		current_board = current_move[1]
		print 'alphabeta - current board', current_board
		# Get the next moves
		next_moves = []
		if  player == 1 and config.timer_ok:
			computed_move = []
			self.our_ia.update_game_graph(current_board)
			next_moves = self.our_ia.find_smart_move()

			# print "next_moves", next_moves
			best_moves = []
			for move in next_moves:
				board = move[0]
				# Keep the current_move[2] means keep the order, which should be the first we have to make to get there
				computed_move = self.alphabeta(-player, (board.score(), board, current_move[2]), depth-1, False, alpha, beta)
				alpha = max(alpha, computed_move[0])
				print 'alphabeta - alpha', alpha
				if beta <= alpha:
					break
				best_moves.append(computed_move)
			best_moves = sorted(best_moves, key=itemgetter(0), reverse=True)
			try:
				return best_moves[0]
			except:
				return []

		elif config.timer_ok:
			computed_move = []
			self.other_ia.update_game_graph(current_board)
			next_moves = self.other_ia.find_smart_move()

			# print "next_moves", next_moves
			best_moves = []
			for move in next_moves:
				board = move[0]
				computed_move = self.alphabeta(player, (board.score(), board, current_move[2]), depth-1, False, alpha, beta)
				beta = min(beta, computed_move[0])
				print 'alphabeta - beta', beta
				if beta <= alpha:
					break
			best_moves = sorted(best_moves, key=itemgetter(0), reverse=True)
			try:
				return best_moves[0]
			except:
				return []
		else:
			# time is out
			print 'time is out'
			return config.best_move