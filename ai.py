from utility import getOurPositions, getEnnemyPositions, getHumanPositions
class Stuxnet():
	""" Class to handle our AI"""
	def __init__(self, arg):
		self.missionList = []
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
		'''
		# Add current element to the stack
		self.stackToEvaluate = self.gameGraph[0]
		while self.stackToEvaluate != []:
			# Get the next element to evaluate
			# For the future we will probably have to implement a .pop() or similar
			currentBoard = self.stackToEvaluate[0]

			# From the possibility (a board) compute the next smart possible moves
			bestMoves = self.findBestMoves(currentBoard)

		nextOrder = self.selectBestMove(bestMoves)
		return nextOrder

	def findBestMoves(self, currentBoard):
		'''
			From a given board, evaluate all the missions in mission list
			Generate all the outputs for this mission and make a first clean
		'''
		ourPositions = getOurPositions(currentBoard)
		ennemyPositions = getEnnemyPositions(currentBoard)
		humanPositions = getHumanPositions(currentBoard)
		# Concatene all positions (we may want to attack ennemies and humans and we may want to rally our friends)
		allPositions = ourPositions + ennemyPositions + humanPositions
		alternatives = []
		for ourPosition in ourPositions:
			for otherPosition in allPositions:
				if otherPosition != ourPosition:
					for mission in self.missionList:
						# if mission complies with case:
						missionResult = self.computeMissionResult(currentBoard, mission, ourPosition, otherPosition)
						missionScore = self.computeMissionScore(missionResult)
						alternatives.append((missionResult, missionScore))
		moves = alternatives.sort()

		moves = []

		bestMoves = self.cleanMoves(moves)
		return bestMoves

	def computeMissionResult(currentBoard, mission, ourPosition, otherPosition):
		'''
			From the current board, the mission and the 2 considered elements compute the targeted board
		'''
		newBoard = {}
		return newBoard
	def computecomputeMissionScore(self, mission):
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