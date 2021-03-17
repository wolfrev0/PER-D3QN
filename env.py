import random as rd

from config import NCOL,NROW,NFOOD,Reward,EPISODE_MAXLEN
from util import dirs,addModVec

class Env:
	def __init__(self):
		pass
	def useCell(self,cell):
		self.empty_cells.remove(cell)
		return cell
	def releaseCell(self,cell):
		self.empty_cells.append(cell)
		return cell
	def getRandomEmptyCell(self):
		return rd.sample(self.empty_cells,1)[0]
		
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
		if not self.snake:
			self.snake.append(self.getRandomEmptyCell())
		for cell in self.snake:
			self.useCell(cell)
		while len(self.foods)<NFOOD:
			self.foods.append(self.useCell(self.getRandomEmptyCell()))
		return self.makeState()

	def makeState(self):
		return {'snake':self.snake,'foods':self.foods,'time':self.time,'done':self.done}

	def getCellType(self,pos):
		if pos in self.snake: return "SNAKE"
		if pos in self.foods: return "FOOD"
		if pos in self.empty_cells: return "EMPTY"
		raise "Cell type couldn't be determined"

	def step(self,action):
		self.time+=1
		if self.done:
			raise "Ended game cannot step"
		
		npos = addModVec(self.snake[-1],dirs[action])
		npos_type=self.getCellType(npos)
		if npos_type=="FOOD":
			self.foods.remove(self.releaseCell(npos))
			self.snake.append(self.useCell(npos))
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
			self.snake.remove(self.releaseCell(self.snake[0]))
			self.snake.append(self.useCell(npos))
			return (self.makeState(),Reward.IDLE)