import numpy as np

class SumTree(object):
	def __init__(self,n):
		self.n=n
		self.tr=np.zeros(2*n)
	
	def upd(self,idx,p):
		idx+=self.n
		self.tr[idx]=p
		while idx:=idx>>1:
			self.tr[idx]=self.tr[idx<<1]+self.tr[idx<<1|1]
		
	def lower_bound(self,psum):
		ti=1
		while ti<self.n:
			if psum<self.tr[ti<<1]:
				ti=ti<<1
			else:
				psum-=self.tr[ti<<1]
				ti=ti<<1|1
		return ti-self.n
	def getval(self,idx): return self.tr[self.n+idx]
	def sumall(self): return self.tr[1]

class PER(object):
	def __init__(self,n,alpha=.6,beta=.4,eps=.01):
		self.n=n
		self.alpha=alpha
		self.beta=beta
		self.eps=eps
		
		self.tree=SumTree(n)
		self.data=np.zeros(n,dtype=object)
		self.cnt=0
	
	def upd(self,idx,td,data):
		p=(abs(td)+self.eps)**self.alpha
		self.tree.upd(idx,p)
		self.data[idx]=data
	
	def push(self,td,data):
		self.upd(self.cnt%self.n,td,data)
		self.cnt+=1
	
	def sample(self,k,epi_ratio):
		s=[]
		max_isw=0.
		b=self.beta*(1-epi_ratio)+epi_ratio
		for i in range(k):
			x=np.random.uniform(i,i+1)/k*self.tree.sumall()
			idx=self.tree.lower_bound(x)
			prob=self.tree.getval(idx)/self.tree.sumall()
			isw=(min(self.cnt,self.n)*prob)**-b
			s.append((idx,isw,self.data[idx]))
			if max_isw<isw: max_isw=isw
		return [(idx,isw/max_isw,data) for (idx,isw,data) in s]