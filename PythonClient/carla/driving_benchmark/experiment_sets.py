from __future__ import print_function

from carla.driving_benchmark.experiment import Experiment
from carla.sensor import Camera
from carla.settings import CarlaSettings

def calculate_time_out(path_distance):
    """
    Function to return the timeout ,in milliseconds,
    that is calculated based on distance to goal.
    This is the same timeout as used on the CoRL paper.
    """

    return ((path_distance / 1000.0) / 10.0) * 3600.0 + 10.0

def get_dynamic_tasks(experiment_set):
    """
    Returns the episodes that contain dynamic obstacles
    """
    dynamic_tasks = set()
    for exp in experiment_set:
        if exp.conditions.NumberOfVehicles > 0 or exp.conditions.NumberOfPedestrians > 0:
            dynamic_tasks.add(exp.task)

    return list(dynamic_tasks)



def build_basic_set():
    # We check the town, based on that we define the town related parameters
    # The size of the vector is related to the number of tasks, inside each
    # task there is also multiple poses ( start end, positions )

    exp_set_dict = {
        'Name': 'BasicExperimentSet',
        'Town02': {'poses': [[[4, 2]], [[37, 76]], [[19, 66]], [[19, 66]]],
                   'vehicles': [0, 0, 0, 15],
                   'pedestrians': [0, 0, 0, 50],
                   'weathers_train': [1],
                   'weathers_validation': [1]

                   },
        'Town01': {'poses': [[[7, 3]], [[138, 17]], [[140, 134]], [[140, 134]]],
                   'vehicles': [0, 0, 0, 20],
                   'pedestrians': [0, 0, 0, 50],
                   'weathers_train': [1],
                   'weathers_validation': [1]

                   }

    }

    # We set the camera
    # This single RGB camera is used on every experiment
    camera = Camera('CameraRGB')
    camera.set(FOV=100)
    camera.set_image_size(800, 600)
    camera.set_position(2.0, 0.0, 1.4)
    camera.set_rotation(-15.0, 0, 0)
    sensor_set = [camera]

    return _build_experiments(exp_set_dict, sensor_set), exp_set_dict


def build_corl2017_set():
    def _poses_town01():
        """
        Each matrix is a new task. We have all the four tasks

        """

        def _poses_straight():
            return [[36, 40], [39, 35], [110, 114], [7, 3], [0, 4],
                    [68, 50], [61, 59], [47, 64], [147, 90], [33, 87],
                    [26, 19], [80, 76], [45, 49], [55, 44], [29, 107],
                    [95, 104], [84, 34], [53, 67], [22, 17], [91, 148],
                    [20, 107], [78, 70], [95, 102], [68, 44], [45, 69]]

        def _poses_one_curve():
            return [[138, 17], [47, 16], [26, 9], [42, 49], [140, 124],
                    [85, 98], [65, 133], [137, 51], [76, 66], [46, 39],
                    [40, 60], [0, 29], [4, 129], [121, 140], [2, 129],
                    [78, 44], [68, 85], [41, 102], [95, 70], [68, 129],
                    [84, 69], [47, 79], [110, 15], [130, 17], [0, 17]]

        def _poses_navigation():
            return [[105, 29], [27, 130], [102, 87], [132, 27], [24, 44],
                    [96, 26], [34, 67], [28, 1], [140, 134], [105, 9],
                    [148, 129], [65, 18], [21, 16], [147, 97], [42, 51],
                    [30, 41], [18, 107], [69, 45], [102, 95], [18, 145],
                    [111, 64], [79, 45], [84, 69], [73, 31], [37, 81]]

        return [_poses_straight(),
                _poses_one_curve(),
                _poses_navigation(),
                _poses_navigation()]

    def _poses_town02():
        def _poses_straight():
            return [[38, 34], [4, 2], [12, 10], [62, 55], [43, 47],
                    [64, 66], [78, 76], [59, 57], [61, 18], [35, 39],
                    [12, 8], [0, 18], [75, 68], [54, 60], [45, 49],
                    [46, 42], [53, 46], [80, 29], [65, 63], [0, 81],
                    [54, 63], [51, 42], [16, 19], [17, 26], [77, 68]]

        def _poses_one_curve():
            return [[37, 76], [8, 24], [60, 69], [38, 10], [21, 1],
                    [58, 71], [74, 32], [44, 0], [71, 16], [14, 24],
                    [34, 11], [43, 14], [75, 16], [80, 21], [3, 23],
                    [75, 59], [50, 47], [11, 19], [77, 34], [79, 25],
                    [40, 63], [58, 76], [79, 55], [16, 61], [27, 11]]

        def _poses_navigation():
            return [[19, 66], [79, 14], [19, 57], [23, 1],
                    [53, 76], [42, 13], [31, 71], [33, 5],
                    [54, 30], [10, 61], [66, 3], [27, 12],
                    [79, 19], [2, 29], [16, 14], [5, 57],
                    [70, 73], [46, 67], [57, 50], [61, 49], [21, 12],
                    [51, 81], [77, 68], [56, 65], [43, 54]]

        return [_poses_straight(),
                _poses_one_curve(),
                _poses_navigation(),
                _poses_navigation()
                ]

    # We check the town, based on that we define the town related parameters
    # The size of the vector is related to the number of tasks, inside each
    # task there is also multiple poses ( start end, positions )

    exp_set_dict = {
        'Name': 'CoRL2017ExperimentSet',
        'Town01': {'poses': _poses_town01(),
                   'vehicles': [0, 0, 0, 20],
                   'pedestrians': [0, 0, 0, 50],
                   'weathers_train': [1, 3, 6, 8],
                   'weathers_validation': [4, 14]

                   },
        'Town02': {'poses': _poses_town02(),
                   'vehicles': [0, 0, 0, 15],
                   'pedestrians': [0, 0, 0, 50],
                   'weathers_train': [1, 3, 6, 8],
                   'weathers_validation': [4, 14]

                   }
    }

    # We set the camera
    # This single RGB camera is used on every experiment
    camera = Camera('CameraRGB')
    camera.set(FOV=100)
    camera.set_image_size(800, 600)
    camera.set_position(2.0, 0.0, 1.4)
    camera.set_rotation(-15.0, 0, 0)
    sensor_set = [camera]

    return _build_experiments(exp_set_dict, sensor_set), exp_set_dict


def _build_experiments(configuration_dict, sensor_set):
    """
        Creates the whole set of experiment objects,
        The experiments created depends on the configuration dict

    """

    # Based on the parameters, creates a vector with experiment objects.
    experiments_vector = []
    print(configuration_dict)
    for town, configs in configuration_dict.items():
        if town != 'Town01' and town != 'Town02':
            continue
        weather_set = set(configs['weathers_train'])
        weather_set.update(configs['weathers_validation'])
        weather_set = list(weather_set)

        poses_tasks = configs['poses']
        vehicles_tasks = configs['vehicles']
        pedestrians_tasks = configs['pedestrians']
        for weather in weather_set:

            for iteration in range(len(poses_tasks)):
                poses = poses_tasks[iteration]
                vehicles = vehicles_tasks[iteration]
                pedestrians = pedestrians_tasks[iteration]

                conditions = CarlaSettings()
                conditions.set(
                    SendNonPlayerAgentsInfo=True,
                    NumberOfVehicles=vehicles,
                    NumberOfPedestrians=pedestrians,
                    MapName=town,
                    WeatherId=weather
                )
                # Add all the cameras that were set for this experiments

                for camera in sensor_set:
                    conditions.add_sensor(camera)

                experiment = Experiment()
                experiment.set(
                    Conditions=conditions,
                    Poses=poses,
                    Task=iteration,
                    Repetitions=1
                )
                experiments_vector.append(experiment)

    return experiments_vector
