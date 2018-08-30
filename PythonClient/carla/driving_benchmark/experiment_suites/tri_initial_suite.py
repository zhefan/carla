'''
Project: /home/zhefanye/catkin_ws/src/carla/PythonClient/carla/driving_benchmark/experiment_suites
Created Date: Monday, August 27th 2018, 12:53:18 pm
Author: Zhefan Ye <zhefanye@gmail.com>
-----
Copyright (c) 2018 TBD
Do whatever you want
'''


from __future__ import print_function

from carla.driving_benchmark.experiment import Experiment
from carla.sensor import Camera
from carla.settings import CarlaSettings

from .experiment_suite import ExperimentSuite


class TRIInitialExperimentSuite(ExperimentSuite):

    @property
    def train_weathers(self):
        return [1]

    @property
    def test_weathers(self):
        return [1]

    def build_experiments(self):
        """
            Creates the whole set of experiment objects,
            The experiments created depends on the selected Town.

        """
        # We check the town, based on that we define the town related parameters
        # The size of the vector is related to the number of tasks, inside each
        # task there is also multiple poses ( start end, positions )
        if self._city_name == 'Town01':
            poses_tasks = [[[31, 49]]]
            vehicles_tasks = [0]
            pedestrians_tasks = [0]
        else:
            print('No such environment, maybe next iteration')

        # We set the camera
        # This single RGB camera is used on every experiment

        camera = Camera('CameraRGB')
        camera.set(FOV=100)
        camera.set_image_size(800, 600)
        camera.set_position(2.0, 0.0, 1.4)
        camera.set_rotation(-15.0, 0, 0)

        # Based on the parameters, creates a vector with experiment objects.
        experiments_vector = []
        for weather in self.weathers:

            for iteration in range(len(poses_tasks)):
                poses = poses_tasks[iteration]
                vehicles = vehicles_tasks[iteration]
                pedestrians = pedestrians_tasks[iteration]

                conditions = CarlaSettings()
                conditions.set(
                    SendNonPlayerAgentsInfo=True,
                    NumberOfVehicles=vehicles,
                    NumberOfPedestrians=pedestrians,
                    WeatherId=weather
                )
                # Add all the cameras that were set for this experiments
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
