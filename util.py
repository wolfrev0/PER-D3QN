from config import NROW,NCOL

dirs=[(1,0),(0,1),(-1,0),(0,-1)]
def addModVec(x,y):
	return ((x[0]+y[0])%NROW,(x[1]+y[1])%NCOL)