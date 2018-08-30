'''
Project: /home/zhefanye/catkin_ws/src/carla/PythonClient
Created Date: Monday, August 27th 2018, 12:34:32 pm
Author: Zhefan Ye <zhefanye@gmail.com>
-----
Copyright (c) 2018 TBD
Do whatever you want
'''

import argparse
import logging

from carla.driving_benchmark import run_driving_benchmark
from carla.driving_benchmark.experiment_suites import TRIInitialExperimentSuite
from carla.agent import ForwardAgent

if __name__ == '__main__':

    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='verbose',
        help='print some extra status information')
    argparser.add_argument(
        '-db', '--debug',
        action='store_true',
        dest='debug',
        help='print debug information')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='localhost',
        help='IP of the host server (default: localhost)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-n', '--log_name',
        metavar='T',
        default='test',
        help='The name of the log file to be created by the benchmark'
    )
    argparser.add_argument(
        '--continue_experiment',
        action='store_true',
        help='If you want to continue the experiment with the same name'
    )

    args = argparser.parse_args()
    args.city_name = 'Town01'  # iteration 1
    if args.debug:
        log_level = logging.DEBUG
    elif args.verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)
    logging.info('listening to server %s:%s', args.host, args.port)

    # We instantiate a forward agent, a simple policy that just set
    # acceleration as 0.9 and steering as zero
    agent = ForwardAgent()

    # We instantiate an experiment suite. Basically a set of experiments
    # that are going to be evaluated on this benchmark.
    experiment_suite = TRIInitialExperimentSuite(args.city_name)

    # Now actually run the driving_benchmark
    run_driving_benchmark(agent, experiment_suite, args.city_name,
                          args.log_name, args.continue_experiment,
                          args.host, args.port)
