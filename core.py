import torch as tc
CUDA_AVAILABLE = tc.cuda.is_available()
DEVICE = tc.device("cuda" if CUDA_AVAILABLE else "cpu")

import matplotlib.pyplot as plt
from IPython import display

def render_inline(env):
	plt.figure(3)
	plt.clf()
	plt.imshow(env.render(mode='rgb_array'))
	plt.axis('off')

	display.clear_output(wait=True)
	display.display(plt.gcf())