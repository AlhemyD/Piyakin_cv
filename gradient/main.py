import numpy as np
import matplotlib.pyplot as plt

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

size = 100
image = np.zeros((size, size, 3), dtype="uint8")
assert image.shape[0] == image.shape[1]

color1 = [255, 255, 255]
color2 = [0, 0, 0]

for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        t=(i+j)/(2*(size-1))
        r = lerp(color2[0], color1[0], t)
        g = lerp(color2[1], color1[1], t)
        b = lerp(color2[2], color1[2], t)
        image[i, j, :] = [r, g, b]

plt.figure(1)
plt.imshow(image)
plt.show()
