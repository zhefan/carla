import os
import numpy as np
import unittest
from carla.driving_benchmark.metrics import Metrics
from carla.driving_benchmark.recording import Recording
import matplotlib.pyplot as plt


def sum_matrix(matrix):
    # Line trick to reduce sum a matrix in one line
    return sum(sum(matrix, []))


class testBenchmark(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(testBenchmark, self).__init__(*args, **kwargs)

        self._metrics_parameters = {

            'intersection_offroad': {'frames_skip': 10,  # Check intersection always with 10 frames tolerance
                                     'frames_recount': 20,
                                     'threshold': 0.3
                                     },
            'intersection_otherlane': {'frames_skip': 10,  # Check intersection always with 10 frames tolerance
                                       'frames_recount': 20,
                                       'threshold': 0.4
                                       },
            'collision_other': {'frames_skip': 10,
                                  'frames_recount': 20,
                                  'threshold': 400
                                  },
            'collision_vehicles': {'frames_skip': 10,
                                   'frames_recount': 30,
                                   'threshold': 400
                                   },
            'collision_pedestrians': {'frames_skip': 5,
                                      'frames_recount': 100,
                                      'threshold': 300
                                      },
            'dynamic_episodes': [3]

        }

    def test_has_agent_collided(self):

        measurement_colision_vec = []

        path = 'test/unit_tests/test_data/testfile_collisions'
        with open(os.path.join(path, 'measurements.csv'), "rU") as f:

            header_metrics = f.readline()
            header_metrics = header_metrics.split(',')
            header_metrics[-1] = header_metrics[-1][:-1]

        measurements_matrix = np.loadtxt(os.path.join(path, 'measurements.csv'), delimiter=",",
                                         skiprows=1)


        car_colision_sequence = measurements_matrix[:, header_metrics.index('collision_vehicles')]
        other_colision_sequence = measurements_matrix[:, header_metrics.index('collision_other')]


        path = 'test/unit_tests/test_data/testfile_collisions'
        with open(os.path.join(path, 'measurements_pedestrians.csv'), "rU") as f:

            header_metrics = f.readline()
            header_metrics = header_metrics.split(',')
            header_metrics[-1] = header_metrics[-1][:-1]

        measurements_matrix = np.loadtxt(os.path.join(path, 'measurements_pedestrians.csv'), delimiter=",",
                                         skiprows=1)


        pedestrian_colision_sequence = measurements_matrix[:, header_metrics.index('collision_pedestrians')]
        plt.plot(pedestrian_colision_sequence)

        plt.show()
