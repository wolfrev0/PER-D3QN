import random
import numpy as np
import copy

from config import NCOL,NROW,NFOOD,Reward,EPISODE_MAXLEN
from util import dirs,addModVec

def stateTransform(state,flipy,flipx,deltay,deltax):
    def fy(y): return (NROW-1-(y+deltay+NROW)%NROW if flipy else y+NROW+deltay)%NROW
    def fx(x): return (NCOL-1-(x+deltax+NCOL)%NCOL if flipx else x+NCOL+deltax)%NCOL
    ret=copy.deepcopy(state)
    ret['snake']=[(fy(y),fx(x)) for y,x in state['snake']]
    ret['foods']=[(fy(y),fx(x)) for y,x in state['foods']]
    return ret
def actTransform(act,flipy,flipx):
    if act%2: return (act+2)%4 if flipx else act #1,3
    else: return (act+2)%4 if flipy else act  #0,2

class Env:
	def __init__(self, flipTransform):
		self.flipTransform=flipTransform
	def useCell(self,cell):
		self.empty_cells.remove(cell)
		return cell
	def releaseCell(self,cell):
		self.empty_cells.append(cell)
		return cell
	def getRandomEmptyCell(self):
		return random.sample(self.empty_cells,1)[0]
		
	def reset(self, obs=None):
		self.empty_cells = [(y,x) for y in range(NROW) for x in range(NCOL)]
		if not obs:
			obs={
				'snake': [],
				'foods': [],
				'time': 0,
				'done': False
			}
		self.snake = obs['snake']
		self.foods = obs['foods']
		self.time = obs['time']
		self.done = obs['done']
		for cell in self.snake:
			self.useCell(cell)
		while len(self.snake)<2:
			self.snake.append(self.useCell(self.getRandomEmptyCell()))
		for cell in self.foods:
			self.useCell(cell)
		while len(self.foods)<NFOOD:
			self.foods.append(self.useCell(self.getRandomEmptyCell()))
		return self.makeState()

	def makeState(self):
		s={'snake':self.snake,'foods':self.foods,'time':self.time,'done':self.done}
		cy,cx=NROW//2,NCOL//2
		hy,hx=self.snake[-1]
		fy = np.random.randint(0,2),np.random.randint(0,2) if self.flipTransform else 0
		fx = np.random.randint(0,2),np.random.randint(0,2) if self.flipTransform else 0
		s=stateTransform(s,fy,fx,cy-hy,cx-hx)
		return s

	def getCellType(self,pos):
		if pos in self.snake: return "SNAKE"
		if pos in self.foods: return "FOOD"
		if pos in self.empty_cells: return "EMPTY"
		raise "Cell type couldn't be determined"

	def step(self,action):
		self.time+=1
		if self.done:
			raise "Ended game cannot step"
		
		#remove tail
		tail=self.snake[0]
		self.snake.remove(self.releaseCell(tail))

		npos = addModVec(self.snake[-1],dirs[action])
		npos_type=self.getCellType(npos)
		if npos_type=="FOOD":
			self.foods.remove(self.releaseCell(npos))
			self.snake.append(self.useCell(npos))
			#restore tail
			self.snake.insert(0,self.useCell(tail))
			
			while len(self.foods)<NFOOD:
				self.foods.append(self.useCell(self.getRandomEmptyCell()))
			return (self.makeState(),Reward.FOOD)
		elif npos_type=="SNAKE":
			self.done=True
			return (self.makeState(),Reward.COLLIDE)
		else: #EMPTY CELL
			if self.time==EPISODE_MAXLEN:
				self.done=True
				return (self.makeState(),Reward.IDLE)
			self.snake.append(self.useCell(npos))
			return (self.makeState(),Reward.IDLE)