import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops, euler_number
from collections import defaultdict
from pathlib import Path

def recognize(region):
    if region.image.mean() == 1.0:
        return "-"
    else:
        enumber = euler_number(region.image, 2)
        if enumber == -1: #B or 8
            have_vl = np.sum(np.mean(region.image[:, :region.image.shape[1]//2], 0)==1) >3
            if have_vl:
                return "B"
            else:
                return "8"
        elif enumber == 0: #A or 0
            image = region.image.copy()
            image[-1, :] = 1            
            enumber = euler_number(image)
            if enumber == -1:
                return "A"
            else:
                min_d_ecc=0.40966657947012936
                max_d_ecc=0.5878823222382653

                min_p_ecc=0.699035125162394
                max_p_ecc=0.7371586900093476
                if min_d_ecc<=region.eccentricity<=max_d_ecc:
                    return "D"
                elif min_p_ecc<=region.eccentricity<=max_p_ecc:
                    return "P"
                else:
                    return "0"

        else: # /, w, x, *, 1
            have_vl = np.sum(np.mean(region.image, 0) == 1) > 3
            if have_vl:
                return "1"
            else:
                if region.eccentricity < 0.4:
                    return "*"
                else:
                    image = region.image.copy()
                    image[0, :] = 1
                    image[-1, :] = 1
                    image[:, 0] = 1
                    image[:, -1] = 1
                    enumber = euler_number(image)
                    if enumber == -1:
                        return "/"
                    elif enumber == -3:
                        return "X"
                    else:
                        return "W"
    return "@"




im = plt.imread("symbols.png")[:,:,:3].mean(2)
im[im>0] =1
labeled = label(im)
plt.imshow(labeled)
#plt.show()
regions = regionprops(labeled)
result = defaultdict(lambda: 0)
path = Path("images")
path.mkdir(exist_ok=True)

for i, region in enumerate(regions):

    #print(i)
    symbol = recognize(region)
    
    result[symbol] += 1
    plt.cla()
    plt.title(f'Symbol-{symbol} - {region.eccentricity}')
    plt.savefig(path / f'image_{i:03d}.png')
print(result)
    
