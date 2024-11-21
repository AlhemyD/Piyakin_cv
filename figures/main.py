import numpy as np
from scipy.ndimage import label, find_objects

shape_order=[]

def analyze_image(binary_array):
    labeled_array, num_features = label(binary_array)    
    shape_count = {}
    
    for i in range(1, num_features + 1):
        obj_slice = find_objects(labeled_array == i)[0]
        obj = binary_array[obj_slice]
        contours = np.argwhere(obj)
        
        shape = f"{obj}"
        
        if shape in shape_count:
            shape_count[shape] += 1
        else:
            shape_count[shape] = 1
            shape_order.append(shape)
            

    return shape_count

binary_image = np.load('ps.npy')
number_of_objects_types = analyze_image(binary_image)
print(f"Общее количество объектов: {sum([number_of_objects_types[i] for i in number_of_objects_types])}")
for i in number_of_objects_types:
    print("\n")
    array=i.split("\n")
    for j in array:
        print(j.replace("[","").replace("]","").replace(" ",""))
    print(f"_____________{number_of_objects_types[i]}")
