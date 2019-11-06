import random

class BlackBoxEnvironment:
	# problem data
	dimension = 0
	initialCarRow = 0
	initialCarColumn = 0
	
	# rewards
	finalReward = 0.0
	localReward = 0.0
	
	# transition probabilities
	probCorrectMove = 0.0
	probWrongMove = 0.0
	
	# possile actions
	actions = ["UP","DOWN","RIGHT","LEFT"]
	
	
	def __init__(self, n, seed, correctProb):
		"""
		constructor
		"""
		self.maze = _getProblemInstance(n, 1, seed)
		self.dimension = n

		# obtainint the initial position of the car
		initialCarRow = 0;

		for c in range(self.dimension):
			if (self.maze[0][c] == 1): # the car
				self.initialCarColumn = c
				break # exiting the loop

		self.probWrongMove = (1.0 - correctProb)/3.0
		self.probCorrectMove = 1.0 - 3.0*self.probWrongMove
		
		self.localReward = -1.0
		self.finalReward = 2.0*self.dimension


	# access methods
	
	def getInitialCarColumn(self):
		return self.initialCarColumn

	def getActions(self):
		return self.actions

	def isGoal(self, row, column):
		'''
		check if a given position (cell) corresponds to a final state or not 
		'''
		if (row == self.dimension-1):
			return True
		else:
			return False

	def getReward(self, row, column):
			'''
		check if a given position (cell) corresponds to a final state or not 
		'''
		if (row == self.dimension-1):
			return finalReward
		else:
			return localReward


	def _getProblemInstance(n, nCars, seed):
	    """
	    method to initialise the environment 
	    """
	    
	    maze = [[0 for i in range(n)] for j in range(n)]
	    #maze = np.zeros((n,n))
	    
	    random.seed(seed)

	    # number of walls
	    nWalls = int(n * (n-2) * 0.2)
			
	    # placing walls
	    for i in range(nWalls):
	        maze[random.randint(0,n-3) + 1][random.randint(0,n-1)] = -1;
			
	    # placing cars, labelled as 1, 2, ..., nCars
	    if (nCars > n):
	    	print("** Error **, number of cars must be <= dimension of maze!!")
	    	sys.exit()

	    list = [i for i in range(n)]

	    for c in range(nCars):
	    	idx = random.randint(0,len(list)-1)
	    	maze[0][list[idx]] = c+1;
	    	list.pop(idx)

	    return maze

	def _getNextPositionsByDeterministicAction(self, row, column):
	    """
		Get next position by action.
		Returns the obtained cells when DETERMINISTICALLY applying each action over the current one
	    """
	    
		next = [[0 for i in range(2)] for j in range(len(self.actions))]
				
		for a in range(len(self.actions)):
			
			next[a][0] = row
			next[a][1] = column
			
			# accion UP
			if (self.actions[a] == "UP") and (row > 0) and (self.maze[row-1][column] >= 0):
				next[a][0] = row-1
			
			# accion DOWN		
			if (self.actions[a] == "DOWN") and (row < (self.dimension-1)) and (self.maze[row+1][column] >= 0):
				next[a][0] = row+1
			
			# accion RIGHT			
			if (self.actions[a] == "RIGHT") and (column < (self.dimension-1)) and (self.maze[row][column+1] >= 0):
				next[a][1] = column+1

			# accion LEFT			
			if (self.actions[a] == "LEFT") and (column > 0) and (self.maze[row][column-1] >= 0):
				next[a][1] = column-1

		return next


	
	def _getActionIndex(self, action):
		'''
	 	get the index in the vector of actions for the passed (string) action
		'''
	
		for i in range(len(self.actions)):
			if (self.actions[i] == action):
				return i;
			
		return -1; # error: not possible action


	def applyAction(self, row, column, action):
		'''
		 Apply action. 
	
		Receives:
	 	   The current cell (row,column)
	 	   The action to be applied (UP,DOWN,RIGHT,LEFT) 
	 	   An initialised random number generator.
	 	
	 	Returns an ArrayList with three objects:
	 	   index=0: row of the obtained cell (int)
	 	   index=1: column of the obtained cell (int)
	 	   index=2: obtained reward (double)
		'''
	
		outcome = [] # newX, newY, reward
		
		next = self._getNextPositionsByDeterministicAction(row,column)
		actionIndex = self._getActionIndex(action)
		
		accProbs = [0.0 for i in range(len(self.actions))]
		acc = 0.0
		for i in range(len(self.actions)): 
			if (i == actionIndex):
				acc += self.probCorrectMove
			else:
				acc += self.probWrongMove
			
			accProbs[i] = acc
		
		accProbs[len(self.actions)-1] = 1.0 # to avoid round errors
		
		r = random.random();
		
		move = -1

		for i in range(len(self.actions)): 
			if (r <= accProbs[i]):
				move = i
				break
		
		outcome.add(next[move][0])
		outcome.add(next[move][1])
		if (self.isGoal(next[move][0],next[move][1])):
			outcome.add(self.finalReward)
		else: 
			outcome.add(self.localReward)
		
		return outcome
	
	def printMaze():
		'''
		Print the input maze.
		'''
		n = len(maze)

		# upper row
		print("-"*n,end='')
		print("--")

		# maze content (by row)
		for j in range(n):
			print("|",end='')
			for i in range(n):
				if (maze[j][i] == -1): 
					print("x",end='')
				elif (maze[j][i] > 0): 
					print(maze[j][i],end='')
				else:
					print(" ",end='')
			print("|")

		# lowe row
		print("-"*n,end='')
		print("--")
	
