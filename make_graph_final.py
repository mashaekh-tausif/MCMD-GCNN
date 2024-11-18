import numpy as np
from ovito.io import import_file
from ovito.data import NearestNeighborFinder
import os
import time
import yaml

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

lmp_directory=config['directories']['lmp_file_directory']
graph_directory=config['directories']['graph_directory']

for temperature in range(350, 1150 + 1, 100):  # normal code 350 to 1450 with 100 interval

    file_template = lmp_directory+f'\\T={temperature}K\\dump.mc.'
    start_time = time.time()

    for i in range(200, 60000 + 1, 200):
        filename = file_template + str(i)
        pipeline = import_file(filename)
        data = pipeline.compute()
        finder = NearestNeighborFinder(12, data)

        property_tensor = np.genfromtxt(filename, skip_header=9, delimiter=' ')  # id,type,x,y,z,vx,vy,vz
        property_tensor = property_tensor[property_tensor[:, 0].argsort()]
        box_dimension = np.genfromtxt(filename, skip_header=5, skip_footer=13501)
        row, column = property_tensor.shape

        id = property_tensor[:, 0] - 1
        type = property_tensor[:, 1]

        final_property_tensor = np.zeros((row, 2))  # id,type

        index_1 = np.arange(0, 13500)

        id1 = data.particles['Particle Identifier'][index_1] - 1

        index_2, _ = finder.find_all()

        id2 = data.particles['Particle Identifier'][index_2] - 1

        id2_flattened = id2.flatten()

        # id2_tiled=np.tile(id2_flattened,len(id1))

        id1_repeat = np.repeat(id1, id2.shape[1])

        edges = np.column_stack((id1_repeat, id2_flattened))


        v = np.sqrt(property_tensor[:, 5] ** 2 + property_tensor[:, 6] ** 2 + property_tensor[:, 7] ** 2) # finding absolue velocity

        final_property_tensor[:,0]=property_tensor[:,1] #type
        final_property_tensor[:,1]=v #velocity

        features = final_property_tensor  # id,type,x,y,z,xs,ys,zs,vx,vy,vz,v

        # list_2d = [list(inner_generator) for inner_generator in generator_2d]


        # features = np.array(features)
        # edges = np.array(edges)
        edges = edges[edges[:, 0].argsort()]
        # edges = np.transpose(edges)

        directory = graph_directory+f'\\T={temperature}K'
        os.makedirs(directory, exist_ok=True)
        feature_path = os.path.join(directory, f'feature.{temperature}K.' + str(i))
        edge_path = os.path.join(directory, f'edge.{temperature}K.' + str(i))
        np.save(edge_path, edges)
        np.save(feature_path, features)
        print(f'dump.{temperature}K.mc.{i}')

        #print(property_tensor)
        #print(features)
        #print(edges)
        print(f'dump.{temperature}K.mc.{i}')

    end_time = time.time()
    runtime = end_time - start_time
    print(f'Runtime = {runtime / 60} minutes')


