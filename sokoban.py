'Fichefet Pierrick 26631000'
'Daubry Benjamin 307910000'
'Goupe #16'
import time
import sys
import operator
from os import listdir,system
from search import *

#################  
# Problem class #
#################

class Sokoban(Problem):
	def __init__(self, init):
		self.size = ()
		self.start=()
		self.createMap(init)
		pass
	
	def goal_test(self, state):
		currentState = tupleToList(state[0])
		stateGoal = state[1]
		boxEndingState = 0
		NumberOfEndingPoint = len(stateGoal)
		for (letter,line,col) in currentState:
			if (letter == '$'):
				for (point,endLine,endCol) in stateGoal:
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
		#state=state[1]
		grid=tupleToList(state[0])
		for elem,line,col in grid:
			if(elem =='@'):
				break;
			i+=1
		ligne=grid[i][1]
		colonne=grid[i][2]
		for col,line in directions:
			newL=ligne+line
			newC=colonne+col
			what=whatIsHere(grid,newL,newC)
			if(canMove(grid,newL,newC,self.size,(line,col))):
				where=0

				if(what=='box'):
					if(blockCorner(grid,newL+line,newC+col,self.size,state[1]) 
						or stuckAgainstWall(grid,newL+line,newC+col,self.size,state[1],(col,line))):
					#if(not stuckAgainstWall(grid,newL+line,newC+col,self.size)):
						continue

					where=findBox(grid,newL,newC)
					newLB=newL+line
					newCB=newC+col
					grid[where][1]=newLB
					grid[where][2]=newCB

				grid[i][1]=newL
				grid[i][2]=newC
				nextState=(listToTuple(grid),state[1],(self.size[0]+2,self.size[1]+2))
				successors.append(((newL,newC),nextState))

				grid[i][1]=ligne
				grid[i][2]=colonne
				if(what=='box'):
					grid[where][1]=newL
					grid[where][2]=newC

		return tuple(successors)

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
		self.initial=((tuple(mapL),tuple(mapLG),(sizeL,sizeC)))
		self.size=(sizeL-2,sizeC-2) #[0 ... sizeC-2]
		f.close
		g.close

###################### 
# Auxiliary function #
######################

directions = [ [-1, 0], [1, 0], [0, -1], [0, 1] ]

def findBox(grid,l,c):
	i=0
	for elem,line,col in grid:
		if(l==line and c==col):
			return i
		i+=1

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

#check if how many boxes reach their goal
def checkBoxOnEndPoint(grid):
	boxReachGoal = []
	state = list(grid[0])
	stateGoal = list(grid[1])
	for letter,line,col in state:
		if(letter == '$'):
			if ('.',line,col) not in stateGoal:
				boxReachGoal.append((letter,line,col))
	return boxReachGoal	


def heuristic(grid):
	grid=grid.state
	state = list(grid[0])
	stateGoal = list(grid[1])
	littleMan = []
	needToChangeDirection = 0
	distManToBox = sys.maxsize
	closestGoal = ()
	distAllBoxToAllTarget = 0
	box = checkBoxOnEndPoint(grid)

	for (letter,line,col) in state:
		if (letter == '@'):
			littleMan.append(line)
			littleMan.append(col)	
			break

	for (letter,line,col) in box:
		if(distManToBox >= abs(littleMan[0]-line)+abs(littleMan[1]-col)-1):
			distManToBox = abs(littleMan[0]-line)+abs(littleMan[1]-col)-1 #-1 because we need to go next to the box not on the box
		
	for (letter,line,col) in box:
		distBoxToTarget = sys.maxsize
		for (point,goalLine,goalCol) in stateGoal:
			if(distBoxToTarget >= abs(line-goalLine)+abs(col-goalCol)):
				distBoxToTarget = abs(line-goalLine)+abs(col-goalCol)
				if(line != goalLine and col != goalCol):
					needToChangeDirection += 1	
				closestGoal = (point,goalLine,goalCol)		
		stateGoal.remove(closestGoal)		
		distAllBoxToAllTarget += distBoxToTarget
	return distManToBox+distAllBoxToAllTarget+(needToChangeDirection*2)

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
def blockCorner(grid,ligne,colonne,sizeMap,goal):
	count=0 
	lr=0
	ud=0
	for col,line in directions:
		newL=ligne+line
		newC=colonne+col
		what=whatIsHere(grid,newL,newC)

		if (('.',ligne,colonne) not in goal):
		 	if(what=='wall' or not (inBounds(grid,(newL,newC),sizeMap))):
		 		count+=1
		 		if(line!=0):
		 			ud+=1
		 		elif(col!=0):
		 			lr+=1
		else:
			return False
	if count>2: # > 2 et pas >= car le bloc n'est bloqué que si les 2 mur qui le touchent, touchent des côté adjacent.	
		return True
	elif count==2:
		if (ud==2 or lr==2):
			return False
		else:
			return True
	else:
		return False

def iswall(grid,newL,newC,size):
	return whatIsHere(grid,newL,newC) == 'wall' or not (inBounds(grid,(newL,newC),size))

def stuckAgainstWall(grid,boxLine,boxCol,size,goal,diir):
	if('.',boxLine,boxCol) not in goal:

		newL = boxLine+diir[1]
		newC = boxCol+diir[0]
		if iswall(grid,newL,newC,size):
			if(diir[1] == 0):
				while(newL < size[0]):
					if ('.',newL,boxCol) in goal or not iswall(grid,newL,newC,size):
						return False
					newL += 1
				newL=boxLine-1
				while(newL >= 0):

					if ('.',newL,boxCol) in goal or not iswall(grid,newL,newC,size) :
						return False
					newL -= 1
			elif(diir[0] == 0):
				while(newC < size[1]):
					if ('.',boxLine,newC) in goal or not iswall(grid,newL,newC,size) :
						return False
					newC += 1
				newC=boxCol-1
				while(newC >= 0):
					if ('.',boxLine,newC) in goal or not iswall(grid,newL,newC,size) :
						return False
					newC -= 1
			return True
		else:
			return False
	else:
		return False

#Mettre coordonnee sans mur exterieur (je pense)
def whatIsHere(grid,ligne,colonne):
	for e in grid:
		if ligne==e[1] and colonne==e[2]:
			if e[0] == '$':
				return 'box'
			elif e[0] =='#':
				return 'wall'
	return 'nothing'


#verifie si on est dans la map sans mur externe (ligne,colonne)
def inBounds(grid, pos,sizeMap):
	return 0 <= pos[0] and pos[0] < sizeMap[0] and 0 <= pos[1] and pos[1] < sizeMap[1]

#mettre colonne+2 et ligne +2 ou sizeC sizeL du createmap (donc VRAI TAILLE AVEC MUR EXTERNE)
def printState(grid,colonne,ligne):
	i=0
	flligne=""
	grid=sorted(grid, key=lambda colonnes: colonnes[1])
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
start_time = time.time()  
problem=Sokoban(sys.argv[1])

node=astar_graph_search(problem,heuristic)
#node=depth_first_graph_search(problem)

path=node.path()
path.reverse()
nNode=0
for n in path:
	nNode+=1
	printState(n.state[0],n.state[2][1],n.state[2][0]) 

interval = time.time() - start_time 
print("number of node (for solution): %d" % nNode) 
print('Total time in seconds:', interval )
