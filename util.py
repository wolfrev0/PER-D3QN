from config import NROW,NCOL,EPISODE_MAXLEN

dirs=[(1,0),(0,1),(-1,0),(0,-1)]
def addModVec(x,y):
	return ((x[0]+y[0])%NROW,(x[1]+y[1])%NCOL)

def state2input(state):
	#4 = shape(1), shape(0~1), Food Pos, time
	ret=[[[0]*NCOL for _ in range(NROW)] for __ in range(4)]
	snake=state['snake']
	for i,(y,x) in enumerate(snake):
			ret[0][y][x]=(i+1)/len(snake)
			ret[1][y][x]=1.
	for y,x in state['foods']:
			ret[2][y][x]=1.
	ret[3]=[[1-state['time']/EPISODE_MAXLEN]*NCOL for _ in range(NROW)]
	return ret