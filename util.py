from config import NROW,NCOL,EPISODE_MAXLEN

dirs=[(1,0),(0,1),(-1,0),(0,-1)]
def addModVec(x,y):
	return ((x[0]+y[0])%NROW,(x[1]+y[1])%NCOL)

def state2input(state):
	#4 = shape, head pos, tailpos, Food Pos, time
	ret=[[[0]*NCOL for _ in range(NROW)] for __ in range(5)]
	snake=state['snake']
	for i,(y,x) in enumerate(snake):
			ret[0][y][x]=(i+1)/len(snake)
	heady,headx = snake[-1]
	ret[1][heady][headx]=1.
	taily,tailx = snake[0]
	ret[2][taily][tailx]=1.
	for y,x in state['foods']:
			ret[3][y][x]=1.
	ret[4]=[[1-state['time']/EPISODE_MAXLEN]*NCOL for _ in range(NROW)]
	return ret