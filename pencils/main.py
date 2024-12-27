import numpy as np
import os
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

pencils=dict()
for file in os.listdir("./images/"):
    pencils.update({file:0})
    image=plt.imread(f"./images/{file}")

    binary=image.mean(axis=2)
    
    binary[binary<=150]=1
    binary[binary>150]=0
    plt.imshow(binary)
    plt.show()
    regions=regionprops(label(binary))
    for region in regions:
        if region.area>250_000 and region.eccentricity>0.95:
            pencils[file]+=1
print("Количество карандашей на каждом изображении:")
for i in pencils:
    print(i, pencils[i])
print("суммарное количество карандашей: ", sum([i for i in pencils.values()]))
