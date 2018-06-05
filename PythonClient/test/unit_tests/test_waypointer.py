
import unittest
import random
import numpy as np
from PIL import  Image

from carla.planner import Waypointer
from carla.planner import Planner
from carla.planner import Converter

from carla.carla_server_pb2 import Transform


def get_posible_start_pixels(town_map_name):
    array = Image.open(town_map_name)
    array.load()
    array = np.asarray(array)
    print (array[:, :, 1])

    return np.transpose(np.nonzero(array[:, :, 1]))




class testWaypointer(unittest.TestCase):


    def __init__(self, *args, **kwargs):

        super(testWaypointer, self).__init__(*args, **kwargs)


    def test_graph_to_waypoints(self):
        # OBS, can also test
        # TOWN01 Test !


        waypointer = Waypointer('Town01')
        planner = Planner('Town01')
        converter = Converter("carla/planner/Town01.txt", 0.1643, 50)
        # Create the test transform positions For all the map positions that are posible.


        start_pixels = get_posible_start_pixels("carla/planner/Town01Lanes.png")
        print (start_pixels)

        np.set_printoptions(threshold=np.nan, linewidth=200)

        for i in start_pixels:
            for k in start_pixels:
                print("Test ", (i[0], i[1]), (k[0], k[1]))
                start_location = converter.convert_to_world((i[0], i[1]))
                end_location = converter.convert_to_world((k[0], k[1]))

                orientation = random.choice([[0.0001, -1.0], [-1.0, 0.0001],
                                             [0.0001, 1.0], [1.0, 0.0001]])

                start_transform = Transform()
                start_transform.location.x = start_location[0]
                start_transform.location.y = start_location[1]
                start_transform.location.z = start_location[2]

                start_transform.orientation.x = orientation[0]
                start_transform.orientation.y = orientation[1]


                orientation = random.choice([[0.0001, -1.0], [-1.0, 0.0001],
                                             [0.0001, 1.0], [1.0, 0.0001]])

                end_transform = Transform()
                end_transform.location.x = end_location[0]
                end_transform.location.y = end_location[1]
                end_transform.location.z = end_location[2]

                end_transform.orientation.x = orientation[0]
                end_transform.orientation.y = orientation[1]


                print (start_transform, end_transform)

                route = planner.compute_route(start_transform, end_transform)

                waypointer.graph_to_waypoints(route._route_nodes)



        # TOWN02 Test !