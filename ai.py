from utility import getOurPositions, getEnnemyPositions, getHumanPositions, findNextMove
import config

class Stuxnet():
	""" Class to handle our AI"""
	def __init__(self, arg):
		self.missionList = ['attack']
		self.gameGraph = []
		self.stackToEvaluate = []

	def updateGameGraph(self, board):
		'''
			Generate the new game graph.
			For now it replaces the current gameGraph with the given board
			TODO:
			- Remind the past
			- Cut only the wrong branches
		'''
		self.gameGraph = [board]
	
	def findSmartMove(self):
		'''
			Called once in the main loop and return the smartest order we could find
			Implementation of the min/max or alpha/beta :)
			For now we make only one round (just findBestMoves actually)
		'''
		# Add current element to the stack
		self.stackToEvaluate = self.gameGraph[0]
		while self.stackToEvaluate != []:
			# Get the next element to evaluate
			# For the future we will probably have to implement a .pop() or similar
			currentBoard = self.stackToEvaluate[0]

			'''For testing purpose, we have to "pop" the element IRL '''
			self.stackToEvaluate = []
			# From the possibility (a board) compute the next smart possible moves
			bestMoves = self.findBestMoves(currentBoard)

			''' IRL we have to add the next elements to evaluate in the stackToEvaluate '''
		nextOrder = self.selectBestMove(bestMoves)
		return nextOrder

	def findBestMoves(self, currentBoard):
		'''
			From a given board, evaluate all the missions in mission list
			And for all the mission, generate all the outputs for this mission and make a first clean
		'''
		ourPositions = getOurPositions(currentBoard)
		ennemyPositions = getEnnemyPositions(currentBoard)
		humanPositions = getHumanPositions(currentBoard)
		# Concatene all positions (we may want to attack ennemies and humans and we may want to join our friends)
		allPositions = []
		# Let's add a tag to remember if the element is our, ennemy or human because we don't want to attack our friend
		for ourPosition in ourPositions:
			allPositions.append((config.nous).extend(ourPosition))
		for ennemyPosition in ennemyPositions:
			allPositions.append((config.eux).extend(ennemyPosition))
		for humanPosition in humanPositions:
			allPositions.append(('h').extend(humanPosition))

		# Receiver for all the alternatives we may find
		alternatives = []

		# Let's go throught all possibilites !
		for ourPosition in ourPositions:
			for otherPosition in allPositions:
				# Let's consider the distincts cases
				if otherPosition != ourPosition:
					for mission in self.missionList:
						# We should not try not attack ourPositions
						if self.isMissionCompliant(otherPosition[0], mission):
							targetBoard, nextOrder = self.computeMissionResult(currentBoard, mission, ourPosition, otherPosition)
							missionScore = self.computeMissionScore(mission, currentBoard, targetBoard)
							alternatives.append((targetBoard, nextOrder, missionScore))
		# Sort the list based on the score
		# moves = alternatives.sort()

		moves = []

		bestMoves = self.cleanMoves(moves)
		return bestMoves

	def isMissionCompliant(self, otherPositionType, mission):
		'''
			From the type of the other position evaluate if the mission makes sense
			For instance 'e', attack will return True but 'o', attack will return False
		'''
		return True

	def computeMissionResult(self, currentBoard, mission, ourPosition, otherPosition):
		'''
			From the current board, the mission and the 2 considered elements compute the targeted board and the next order
		'''
		newBoard = currentBoard
		nextOrder = []
		ourCoordinnates = ourPosition[0]
		ourNumber = ourPosition[1]
		theirType = otherPosition[0]
		theirCoordinnates = otherPosition[1]
		theirNumber = otherPosition[2]

		if mission == 'attack':
			# Remove our position from the board, format of ourPosition ('coordonees', 'nombre')
			del newBoard[ourCoordinnates]
			# Remove their position from the board, format of otherPosition ('type', 'coordonees', 'nombre')
			del newBoard[theirCoordinnates]
			# Add our team on the ennemy position
			if theirType == 'h':
				newBoard[theirCoordinnates] = ('n', ourNumber + )
			else:
				newBoard[otherPosition[1]] = ('n', ourPosition[1])
			nextCoord = findNextMove(ourPosition[0], otherPosition[1])
			nextOrder = ['MOV', otherPosition]
		else:
			pass
		
		return newBoard, nextOrder

	def computeMissionScore(self, mission, currentBoard, targetBoard):
		'''
			Compute the score of a given mission, based on the heuristic function 
		'''
		return 0

	def cleanMoves(self, moves):
		'''
			From a list of moves, keeps only the best ones (TOP 5 or only those with a given score...)
		'''
		bestMoves = []
		return bestMoves

	def selectBestMove(self, bestMoves):
		'''
			Once we have computed all the possible move, select the best one
		'''
		nextOrder = []
		return nextOrder