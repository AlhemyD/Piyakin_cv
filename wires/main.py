import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.ndimage import label, binary_erosion

def analyze_wires(binary_image):    
    labeled_array, num_features = label(binary_image)

    wire_parts = dict()
    for i in range(1, num_features + 1):
        
        defective=np.sum(labeled_array == i,axis=0).max()!=3
        
        wire=labeled_array==i
        
        eroded_wire=np.array(binary_erosion(wire,np.ones((np.sum(labeled_array == i,axis=0).max(),1))),dtype="uint8")
        
        count_segments=[]
        
        for j in eroded_wire:            
            count_segments.append(len(j[j==0])+1)

        count_segments=min(count_segments)
    
        
        wire_parts[i] = {
            'count_segments': count_segments,
            'defective': defective
        }
    
    return num_features, wire_parts
def analyze_images_in_directory(directory_path):
    results = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.npy'):
            image_path = os.path.join(directory_path, filename)

            image = np.load(image_path)

            
            num_wires, wire_parts = analyze_wires(image)
            
            results[filename] = {
                'num_wires': num_wires,
                'wire_parts': wire_parts
            }
            

    return results


directory_path = 'files'
results = analyze_images_in_directory(directory_path)

for filename, data in results.items():
    print(f'Изображение: {filename}')
    print(f'Количество проводов: {data["num_wires"]}')
    for wire_id, segment_data in data["wire_parts"].items():
        print(f'  Провод {wire_id}: Количество частей: {segment_data["count_segments"]}, Дефектный: {segment_data["defective"]}\n')
