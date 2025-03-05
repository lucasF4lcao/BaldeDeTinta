from PIL import Image
import numpy as np

arr = np.loadtxt('../saida.txt', dtype=np.uint8)

img = Image.fromarray(arr, mode='L')

img.save('../imgs/imagem_reconstruida.png')
img.show()
