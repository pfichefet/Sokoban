'Fichefet Pierrick 26631000'
'Daubry Benjamin 307210000'
'Goupe #16'
import time
import sys
from os import listdir,system
from search import *

#################  
# Problem class #
#################

class Sokoban(Problem):
	def __init__(self, init):
		self.stateGoal = []
		self.size = {}
		self.createMap(init)
		pass
	
	def goal_test(self, state):
		boxEndingState = 0
		NumberOfEndingPoint = len(self.stateGoal)
		for (letter,line,col) in state:
			if (letter == '$'):
				for (point,endLine,endCol) in self.stateGoal:
					if(line == endLine and col == endCol):
						boxEndingState += 1
						break
		if (NumberOfEndingPoint == boxEndingState):
			return True
		else:
			return False
	
	def successor(self, state): #state = (  ( (currentLisLetter),(currentPointLine,currentPointCol) ),(grid)  )
		# successors = []
		# currentListLetter = state[0][0]
		# currentLetter = state[0][0][0]
		# currentStartPoint = state[0][1]
		# grid = tupleToList(state[1])
		# for elem in self.end:
		# 	if elem[0] == currentLetter:
		# 		currentEndPoint = (elem[1],elem[2])
		# 		break 		
		# choice = chooseLetter(grid,currentLetter,currentStartPoint,currentEndPoint,currentListLetter,self.start,self.end)
		# currentListLetter = choice[0] #ChooseLetter check if we need to change the current letter or not.			
		# currentLetter = choice[0][0]  
		# currentStartPoint = choice[1]
		# currentEndPoint = choice[2]		
		# for diir in directions:
		# 	nextline = currentStartPoint[0]+diir[1]
		# 	nextcol = currentStartPoint[1]+diir[0]
		# 	if(pathExists(grid,[nextline,nextcol],currentEndPoint) and grid[nextline][nextcol]=='.'):
		# 		grid[nextline][nextcol] = currentLetter
		# 		if(possible(grid,self.start,self.end,list(currentListLetter),currentLetter,(nextline,nextcol))):
		# 			nextState = ((currentListLetter,(nextline,nextcol)),listToTuple(grid))
		# 			successors.append( (diir,nextState  ) )
		# 		grid[nextline][nextcol] = '.'
		# return tuple(successors)
		pass

	def createMap(self,path):
		mapL=[]
		mapLG=[]
		f=open(path+'.init','r')
		sizeL=0
		for line in f:
			sizeL+=1
		f.close
		f=open(path+'.init','r')
		g=open(path+'.goal','r')
		ligne=0
		sizeC=0
		for line,lineG in zip(f,g):
			sizeC=len(line)-1
			colonne=0
			for col,colG in zip(line,lineG):
				if(colonne != 0 and colonne != sizeC-1 and ligne !=0 and ligne != sizeL-1):
					if(col!= '\n' and col!=' '):
						mapL.append((col,ligne-1,colonne-1))
					if(colG=='.'):
						mapLG.append((colG,ligne-1,colonne-1))
				colonne=colonne+1
			ligne=ligne+1
		self.initial=tuple(mapL)
		self.stateGoal=tuple(mapLG)
		self.size['line']=sizeL-2 #[0 ... sizeC-2]
		self.size['col']=sizeC-2
		print('heuristic =', heuristic(tuple(mapL),self.stateGoal))
		print(mapL)
		print(mapLG) 
		print(sizeL,sizeC)
		printState(mapL,sizeC,sizeL)
		printState(mapLG,sizeC,sizeL)
		f.close
		g.close


###################### 
# Auxiliary function #
######################

directions = [ [-1, 0], [1, 0], [0, -1], [0, 1] ]

def tupleToList(yuple):
	llist = []
	for line in yuple:
		llist.append(list(line))
	return llist

def listToTuple(List):
	Tuple = []
	for line in List:
		Tuple.append(tuple(line))
	return tuple(Tuple)	

def heuristic(grid, stateGoal):
	littleMan = []
	box = []
	distManToBox = sys.maxsize
	distBoxToTarget = sys.maxsize
	for (letter,line,col) in grid:
		if (letter == '$'):
			box.append((letter,line,col))
		elif (letter == '@'):
			littleMan.append(line)
			littleMan.append(col)
	print('littleMan =',littleMan)		
	for (letter,line,col) in box:
		if(distManToBox >= abs(littleMan[0]-line)+abs(littleMan[1]-col)):
			lineBox = line
			colBox = col
			distManToBox = abs(littleMan[0]-line)+abs(littleMan[1]-col)
	for (point,letter,col) in stateGoal:
		if(distBoxToTarget >= abs(lineBox-line)+abs(colBox-col)):
			distBoxToTarget = abs(lineBox-line)+abs(colBox-col)
	return distBoxToTarget+distManToBox


#Mettre coordonnee sans mur exterieur (je pense)
def whatIsHere(grid,ligne, colonne):
	for e in grid:
		if ligne==e[1] and colonne==e[2]:
			if e[0] == '$':
				return 'box'
			elif e[0] =='#':
				return 'wall'
			else:
				return 'us' #probably useless
	return 'nothing'

def pathExists(grid, start, end):
	visited = [ [0 for j in range(0, len(grid[0]))] for i in range(0, len(grid)) ]
	ok = pathExistsDFS(grid, start, end, visited)
	return ok

def pathExistsDFS(grid, start, end, visited):
	for d in directions:
		i = start[0] + d[0]
		j = start[1] + d[1]
		next = [i, j]
		if i == end[0] and j == end[1]:
			return True
		if inBounds(grid, next) and grid[i][j] == '.' and not visited[i][j]:
			visited[i][j] = 1
			exists = pathExistsDFS(grid, next, end, visited)
			if exists:
				return True
	return False

def inBounds(grid, pos):
	return 0 <= pos[0] and pos[0] < len(grid) and 0 <= pos[1] and pos[1] < len(grid[0])

#mettre colonne+2 et ligne +2 ou sizeC sizeL du createmap (donc VRAI TAILLE AVEC MUR EXTERNE)
def printState(state,colonne,ligne):
	i=0
	flligne=""
	while(i<colonne):
		flligne+='#'
		i+=1
	print(flligne)
	l=[' ']*colonne
	l[0]='#'
	l[colonne-1]='#'
	tempL=1
	sizestate=len(state)
	last=1
	for e in state:
		line=e[1]
		col=e[2]
		elem=e[0]
		if line+1>tempL:
			print(''.join(l))
			j=tempL
			l=[' ']*colonne
			l[0]='#'
			l[colonne-1]='#'
			while j<line:
				print(''.join(l))
				j+=1
			tempL=line+1

			l[col+1]=elem
			if(last==sizestate):
				print(''.join(l))
		else:
			l[col+1]=elem
			tempL=line+1
		last+=1
	j=tempL
	l=[' ']*colonne
	l[0]='#'
	l[colonne-1]='#'
	# while(j<colonne-1):
	# 	print(''.join(l))
	# 	j+=1
	print(flligne)
	print("")
#####################
# Launch the search #
#####################
#start_time = time.time()  
problem=Sokoban(sys.argv[1])
#example of bfs search
#node=breadth_first_graph_search(problem)
#node=depth_first_graph_search(problem)
#example of print
#path=node.path()
#path.reverse()
#for n in path:
#	printState(n.state) #assuming that the __str__ function of states output the correct format

#interval = time.time() - start_time  
#print('Total time in seconds:', interval )
