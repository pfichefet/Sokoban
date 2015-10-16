'Fichefet Pierrick 26631000'
'Daubry Benjamin 307910000'
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
		self.size = ()
		self.start=()
		self.createMap(init)
		pass
	
	def goal_test(self, state):
		boxEndingState = 0
		NumberOfEndingPoint = len(self.stateGoal)
		for (letter,line,col) in state[1]:
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
		successors = []
		i=0
		grid=list(state[1])
		for elem,line,col in grid:
			if(elem =='@'):
				break;
			i+=1
		ligne=grid[i][1]
		colonne=grid[i][2]
		for col,line in directions:
			newL=ligne+line
			newC=colonne+col
			if(canMove(grid,newL,newC,self.size,(line,col))):
				grid[i][1]=newL
				grid[i][2]=newC
				successors.append((newL,newC),tuple(grid))


#def canMove(grid,ligne,colonne,sizeMap,diir):
#def moveChar(grid,newL,newC):
#def heuristic(grid, stateGoal):
#def blockCorner(grid,ligne,colonne,sizeMap):
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
						if(col=='@'):
							self.start=(ligne-1,colonne-1)
					if(colG=='.'):
						mapLG.append((colG,ligne-1,colonne-1))
				colonne=colonne+1
			ligne=ligne+1
		self.initial=((0,0),tuple(mapL))
		self.stateGoal=tuple(mapLG)
		self.size=(sizeL-2,sizeC-2) #[0 ... sizeC-2]
		print('heuristic =', heuristic(tuple(mapL),self.stateGoal))
		print(mapL)
		print(mapLG) 
		print(sizeL,sizeC)
		uh=blockCorner(mapL,0,1,(sizeL-2,sizeC-2))
		print(uh)
		printState(mapL,sizeC,sizeL)
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
	print(stateGoal)
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
	for (letter,line,col) in box:
		if(distManToBox >= abs(littleMan[0]-line)+abs(littleMan[1]-col)):
			lineBox = line
			colBox = col
			distManToBox = abs(littleMan[0]-line)+abs(littleMan[1]-col)-1 #-1 because we need to go next to the box not on the box
			print(distManToBox)
	for (point,goalLine,goalCol) in stateGoal:
		if(distBoxToTarget >= abs(lineBox-goalLine)+abs(colBox-goalCol)):
			if(lineBox == goalLine or colBox == goalCol):
				distBoxToTarget = abs(lineBox-goalLine)+abs(colBox-goalCol)
			else:
				distBoxToTarget = abs(lineBox-goalLine)+abs(colBox-goalCol)+2 #need to go against an other side of the box
	return distBoxToTarget+distManToBox

def canMove(grid,ligne,colonne,sizeMap,diir):
	what=whatIsHere(grid,ligne,colonne)
	if what=='wall' or not inBounds(grid,(ligne,colonne),sizeMap):
		return False
	if what=='box':
		newL=ligne+diir[0]
		newC=colonne+diir[1]
		what2=whatIsHere(grid,newL,newC)
		if what2=='wall' or what2=='box' or not inBounds(grid,(newL,newC),sizeMap):
			return False
		else:
			return True
	else:
		return True

#si touche 2 mur, cas useless (test pas encore si ya une boite qui bloque (vu quon peut ptet la bouger))
def blockCorner(grid,ligne,colonne,sizeMap):
	count=0 
	lr=0
	ud=0
	for col,line in directions:
		newL=ligne+line
		newC=colonne+col
		what=whatIsHere(grid,newL,newC)
		if what=='wall' or not (inBounds(grid,(newL,newC),sizeMap)):
			count+=1
			if(line!=0):
				ud+=1
			elif(col!=0):
				lr+=1
	if count>2: # > 2 et pas >= car le bloc n'est bloqué que si les 2 mur qui le touchent, touchent des côté adjacent.	
		return True
	elif count==2:
		if (ud==2 or lr==2):
			return False
		else:
			return True
	else:
		return False

def stuckAgainstWall(grid,boxLine,boxCol):
	for diir in directions:
		newL = boxLine+diir[0]
		newC = boxCol+diir[1]
		if(whatIsHere(grid,newL,newC) == 'wall'):
			if(diir[0] == 0):
				while(newL < self.size[0]+2):
					newL += 1
					if(whatIsHere(grid,newL,newC) != 'wall' and whatIsHere(grid,newL,newC) != 'box')
						return False
				while(newL > 0):
					newL -= 1
					if(whatIsHere(grid,newL,newC) != 'wall' and whatIsHere(grid,newL,newC) != 'box')
						return False
			elif(diir[1] == 0):
				while(newC < self.size[1]+2):
					newL += 1
					if(whatIsHere(grid,newL,newC) != 'wall' and whatIsHere(grid,newL,newC) != 'box')
						return False
				while(newC > 0):
					newL -= 1
					if(whatIsHere(grid,newL,newC) != 'wall' and whatIsHere(grid,newL,newC) != 'box')
						return False
	return True

#Mettre coordonnee sans mur exterieur (je pense)
def whatIsHere(grid,ligne,colonne):
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

#verifie si on est dans la map sans mur externe (ligne,colonne)
def inBounds(grid, pos,sizeMap):
	return 0 <= pos[0] and pos[0] < sizeMap[0] and 0 <= pos[1] and pos[1] < sizeMap[1]

#mettre colonne+2 et ligne +2 ou sizeC sizeL du createmap (donc VRAI TAILLE AVEC MUR EXTERNE)
def printState(grid,colonne,ligne):
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
	sizestate=len(grid)
	last=1
	for e in grid:
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
			if(last==sizestate):
				print(''.join(l))
		last+=1
	#j=state[sizestate-1][1]
	j=tempL
	l=[' ']*colonne
	l[0]='#'
	l[colonne-1]='#'
	while(j<ligne-2):
		print(''.join(l))
		j+=1
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
