import time as timelib

from IPython import display
from PIL import Image
from PIL import ImageDraw
from torchvision import transforms
import matplotlib.pyplot as plt
import numpy as np

from config import NCOL,NROW

def render(obs,sleep_time=0,clear=True):
    #print(obs)
    txt = Image.new("RGBA", (NCOL*30,NROW*30), (10,50,100,100))
    draw = ImageDraw.Draw(txt)
    grid_size = 30
    for i in range(NROW):
        for j in range(NCOL):
            y1 = i*grid_size
            x1 = j*grid_size
            y2 = (i+1)*grid_size
            x2 = (j+1)*grid_size
            draw.rectangle(((x1, y1), (x2, y2)), outline='black', width=1)
    for y,x in obs['state']['foods']:
        draw.ellipse((x*grid_size, y*grid_size, (x+1)*grid_size, (y+1)*grid_size), fill = 'yellow', outline ='yellow')
    color_list = ['red', 'green', 'blue', 'purple']
    for i, geese in enumerate(obs['state']['geese']):
        for y,x in geese:
            if (y,x)==geese[-1]:
                draw.polygon([((x+1/2)*grid_size,y*grid_size),(x*grid_size,(y+1/2)*grid_size),
                              ((x+1/2)*grid_size,(y+1)*grid_size), ((x+1)*grid_size,(y+1/2)*grid_size)], fill = color_list[i])
            else:
                draw.rectangle(((x*grid_size, y*grid_size), ((x+1)*grid_size, (y+1)*grid_size)), fill=color_list[i], outline=color_list[i])
    txt = txt.resize((64, 64*7//11)).convert('RGB')
    numpy_image = np.array(txt)
    plt.axis("off")
    trans1 = transforms.ToTensor()
    tensor_image = trans1(numpy_image)
    tf = transforms.ToPILImage()
    plt.imshow(tf(tensor_image))
    plt.show()
    plt.close()
    if sleep_time:
        timelib.sleep(sleep_time)
    if clear:
        display.clear_output(wait=True)
    return tensor_image