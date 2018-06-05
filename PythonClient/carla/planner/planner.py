# Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import collections
import math

import numpy as np

from . import city_track
from .route import Route


def compare(x, y):
    return collections.Counter(x) == collections.Counter(y)



# Constants Used for the high level commands




# Auxiliary algebra function
def angle_between(v1, v2):
    return np.arccos(np.dot(v1, v2) / np.linalg.norm(v1) / np.linalg.norm(v2))


def sldist(c1, c2): return math.sqrt((c2[0] - c1[0]) ** 2 + (c2[1] - c1[1]) ** 2)





class Planner(object):

    def __init__(self, city_name):

        # TODO: This city track concept in my opinion is a little bit bad. We could refactor
        self._city_track = city_track.CityTrack(city_name)

        self._commands = []
        self._city_name = city_name


    def compute_route(self, source_transform, target_tranform):

        # Convert to a neutral format
        source = (source_transform.location.x, source_transform.location.y, source_transform.location.z)
        source_ori = (source_transform.orientation.x,
                      source_transform.orientation.y, source_transform.orientation.z)
        target = (target_tranform.location.x,
                  target_tranform.location.y, target_tranform.location.z)
        target_ori = (target_tranform.orientation.x,
                      target_tranform.orientation.y, target_tranform.orientation.z)

        track_source = self._city_track.project_node(source)
        track_target = self._city_track.project_node(target)

        print(track_source)
        print(track_target)
        print(source_ori)
        print(target_ori)
        route = self._city_track.compute_route(track_source, source_ori,
                                               track_target, target_ori)
        if route is None:
            raise RuntimeError('Impossible to find route')

        return Route(route, self._city_track.get_intersection_nodes(), self._city_name)



    def get_next_command(self, source, source_ori, target, target_ori):
        """
        Computes the full plan and returns the next command,
        Args
            source: source position
            source_ori: source orientation
            target: target position
            target_ori: target orientation
        Returns
            a command ( Straight,Lane Follow, Left or Right)
        """


        track_source = self._city_track.project_node(source)
        track_target = self._city_track.project_node(target)

        # reach the goal

        if self._city_track.is_at_goal(track_source, track_target):
            return REACH_GOAL

        if (self._city_track.is_at_new_node(track_source)
                and self._city_track.is_away_from_intersection(track_source)):

            route = self._city_track.compute_route(track_source, source_ori,
                                                   track_target, target_ori)
            if route is None:
                raise RuntimeError('Impossible to find route')

            self._commands = self._route_to_commands(route)

            if self._city_track.is_far_away_from_route_intersection(
                    track_source):
                return LANE_FOLLOW
            else:
                if self._commands:
                    return self._commands[0]
                else:
                    return LANE_FOLLOW
        else:

            if self._city_track.is_far_away_from_route_intersection(
                    track_source):
                return LANE_FOLLOW

            # If there is computed commands
            if self._commands:
                return self._commands[0]
            else:
                return LANE_FOLLOW

    def get_shortest_path_distance(
            self,
            source,
            source_ori,
            target,
            target_ori):

        distance = 0
        track_source = self._city_track.project_node(source)
        track_target = self._city_track.project_node(target)

        current_pos = track_source

        route = self._city_track.compute_route(track_source, source_ori,
                                               track_target, target_ori)
        # No Route, distance is zero
        if route is None:
            return 0.0

        for node_iter in route:
            distance += sldist(node_iter, current_pos)
            current_pos = node_iter

        # We multiply by these values to convert distance to world coordinates
        return distance * self._city_track.get_pixel_density() \
               * self._city_track.get_node_density()

    def is_there_posible_route(self, source, source_ori, target, target_ori):

        track_source = self._city_track.project_node(source)
        track_target = self._city_track.project_node(target)

        return not self._city_track.compute_route(
            track_source, source_ori, track_target, target_ori) is None

    def test_position(self, source):

        node_source = self._city_track.project_node(source)

        return self._city_track.is_away_from_intersection(node_source)

