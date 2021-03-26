import torch as tc
import torch.nn as nn
import torch.nn.init as init
from config import NROW,NCOL
from core import DEVICE

class Conv(nn.Module):
	def __init__(self, chn_in, chn_out, ker_sz=3):
		super().__init__()
		self.c=nn.Conv2d(chn_in,chn_out,ker_sz,padding=ker_sz//2,padding_mode="circular",bias=False)
		self.b=nn.BatchNorm2d(chn_out)
		self.a=nn.LeakyReLU(0.1)

	def forward(self, x):
		return self.a(self.b(self.c(x)))

class Resi(nn.Module):
	def __init__(self, chn, ker_sz=3):
		super().__init__()
		self.pre=nn.Sequential(
			nn.Conv2d(chn,chn,ker_sz,padding=ker_sz//2,padding_mode="circular",bias=False),
			nn.BatchNorm2d(chn),
			nn.LeakyReLU(0.1),
			nn.Conv2d(chn,chn,ker_sz,padding=ker_sz//2,padding_mode="circular",bias=False),
			nn.BatchNorm2d(chn),
		)
		self.post=nn.LeakyReLU(0.1)

	def forward(self, x):
		return self.post(self.pre(x)+x)
	
class Full(nn.Module):
	def __init__(self, N_in, N_out, afunc=nn.LeakyReLU(0.1), drop_out=False):
		super().__init__()
		self.l=nn.Linear(N_in,N_out)
		self.drop_out=drop_out
		if self.drop_out: self.d=nn.Dropout(0.5)
		self.a=afunc

	def forward(self, x):
		x=self.l(x)
		if self.drop_out: x=self.d(x)
		return self.a(x)

class SnakeNet(nn.Module):
	def __init__(self):
		super(SnakeNet,self).__init__()
		self.chn_in=4
		self.chn_mid=64
		self.chn_out=8

		self.feature=nn.Sequential(
			Conv(self.chn_in,self.chn_mid),
			Resi(self.chn_mid),
			Resi(self.chn_mid),
			Resi(self.chn_mid),
			Resi(self.chn_mid),
			Resi(self.chn_mid),
			Conv(self.chn_mid,self.chn_out),
			nn.Flatten(),
		)
		self.adv = nn.Sequential(
			Full(self.chn_out*NROW*NCOL,256),
			Full(256,4,None),
		)
		self.stval = nn.Sequential(
			Full(self.chn_out*NROW*NCOL,256),
			Full(256,1,None),
		)
		for x in self.modules():
			if isinstance(x,nn.Conv2d) or isinstance(x,nn.Linear):
				init.xavier_uniform_(x.weight.data)
				if x.bias != None:
					init.zeros_(x.bias)

	def forward(self,x):
		x = x.reshape(-1,self.chn_in,NROW,NCOL)
		x = self.feature(x)
		adv = self.adv(x)
		stval = self.stval(x)
		qval = (adv-adv.mean())+stval
		return qval