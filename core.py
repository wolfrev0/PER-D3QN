import torch as tc
CUDA_AVAILABLE = tc.cuda.is_available()
DEVICE = tc.device("cuda" if CUDA_AVAILABLE else "cpu")

import matplotlib.pyplot as plt
from IPython import display