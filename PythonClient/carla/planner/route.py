import numpy as np


from carla.util import signal
from .waypointer import Waypointer

REACH_GOAL = 0.0
GO_STRAIGHT = 5.0
TURN_RIGHT = 4.0
TURN_LEFT = 3.0
LANE_FOLLOW = 2.0


class Route:

    def __init__(self, route_nodes, intersection_nodes, city_name):


        self._route_nodes = route_nodes
        self._intersection_nodes = intersection_nodes
        # TODO: City name is likely to be changed by a description
        self._city_name = city_name
        self._waypointer = Waypointer(city_name)






    def waypoints(self, number_of_waypoints):
        """
        Based on the computed route object
        Returns a list of waypoints depending on the desired configuration.
        ARGS
            The number of next parameters to be used.

        """


        track_source = self._city_track.project_node(source)
        track_target = self._city_track.project_node(target)

        if math.fabs(target_ori[0]) > math.fabs(target_ori[1]):
            target_ori = (target_ori[0], 0.0, 0.0)
        else:
            target_ori = (0.0, target_ori[1], 0.0)

        if math.fabs(source_ori[0]) > math.fabs(source_ori[1]):
            source_ori = (source_ori[0], 0.0, 0.0)
        else:
            source_ori = (0.0, source_ori[1], 0.0)

        # print ''

        # print self.grid

        # reach the goal
        if track_source == track_target:
            return self.last_trajectory

        # This is to avoid computing a new route when inside the route

        distance_node = self._city_track.get_distance_closest_node_turn(track_source)

        if self.debug:
            self._write_point_on_map(self._converter.convert_to_pixel(source), [255, 0, 255, 255],
                                     size=7)

            self._write_point_on_map(self._converter.convert_to_pixel(target), [255, 255, 255, 255],
                                     size=6)

        # If you actually changed the position from a route.
        if distance_node > 2 and self._previous_source != track_source:

            # print node_source
            # print node_target
            #self._route = self._city_track.compute_route(track_source, source_ori, track_target,
            #                                             target_ori)

            # print self._route

            # IF needed we add points after the objective, that is very hacky.
            # TODO: make sure the add extra points function is eliminated.
            #self.add_extra_points(track_target, target_ori, track_source)

            # print added_walls
            if self.debug:
                self.search_image = self._map.map_image.astype(np.uint8)

            self.points = self._waypointer.graph_to_waypoints(
                self._route[1:(1 + self.way_key_points_predicted)])

            self.last_trajectory, self.last_map_points = self.generate_final_trajectory(
                [np.array(self._converter.convert_to_pixel(source))] + self.points)

            return self.last_trajectory  # self.generate_final_trajectory([np.array(self.make_map_world(source))] +self.points)


        else:
            if distance(self.previous_map, self._converter.convert_to_pixel(source)) > 3.0:

                # That is because no route was ever computed. This is a problem we should solve.
                """
                if not self._route:
                    self._route = self._city_track.compute_route(track_source, source_ori,
                                                                 track_target, target_ori)
                    # print self._route

                    self.add_extra_points(track_target, target_ori, track_source)
                    # print added_walls
                    if self.debug:
                        self.search_image = self._map.map_image.astype(np.uint8)
                    self.points = self.graph_to_waypoints(
                        self._route[1:(1 + self.way_key_points_predicted)],
                        self._converter.convert_to_pixel(source))

                    self.last_trajectory, self.last_map_points = self.generate_final_trajectory(
                        [np.array(self._converter.convert_to_pixel(source))] + self.points)
                """

                # We have to find the current node position
                self.previous_map = self._converter.convert_to_pixel(source)
                # Make a source not replaced
                # self.last_trajc,self.last_map_points = self.generate_final_trajectory([np.array(self.make_map_world(source))] +self.points)

                # self.last_trajc = self.generate_final_trajectory([np.array(self.make_map_world(source))] +self.points[(index_source):])
                # self.test = self.generate_final_trajectory([np.array(self.make_map_world(source))] +self.points[(index_source):])

                # What is this part ??
                for point in self.last_map_points:
                    point_vec = self._get_unit(np.array(self._converter.convert_to_pixel(source)),
                                               point)
                    cross_product = np.cross(source_ori[0:2], point_vec)

                    # aux = point_vec[1]
                    # point_vec[1]= point_vec[0]
                    # point_vec[0]= aux

                    # print point_vec,source_ori[0:2]
                    # print cross_product,sldist(point,self.make_map_world(source))

                    if (cross_product > 0.0 and sldist(point, self._converter.convert_to_pixel(
                            source)) < 50) or sldist(
                            point,
                            self._converter.convert_to_pixel(
                                source)) < 15.0:
                        # print 'removed ',self.last_map_points.index(point),self.last_trajc.index(self.make_world_map(point))

                        self.last_trajectory.remove(
                            self._converter.convert_to_world(
                                point))  # = [self.make_world_map(point)] + self.last_trajc
                        self.last_map_points.remove(point)
                # print self.last_map_points
                # print point
                # print 'INDED', np.argwhere(self.last_map_points==point)
                # self.last_map_points.remove(point)
                if self.debug:
                    self._print_trajectory(self.last_map_points, [255, 0, 0, 255], 4)

                    self._print_trajectory(self.points, [255, 128, 0, 255], 7)

            return self.last_trajectory



    # TODO: This has to be kind of a property

    def commands(self):
        """
        Returns a list of commands for this specific route object.
        The current command set is
        STRAIGHT
        LEFT
        RIGHT


        """


        commands_list = []

        for i in range(0, len(self._nodes)):
            if self.route[i] not in self._city_track.get_intersection_nodes():
                continue

            current = self.route[i]
            past = self.route[i - 1]
            future = self.route[i + 1]

            past_to_current = np.array(
                [current[0] - past[0], current[1] - past[1]])
            current_to_future = np.array(
                [future[0] - current[0], future[1] - current[1]])
            angle = signal(current_to_future, past_to_current)

            if angle < -0.1:
                command = TURN_RIGHT
            elif angle > 0.1:
                command = TURN_LEFT
            else:
                command = GO_STRAIGHT

            commands_list.append(command)

        return commands_list

    def next_command(self):
        pass


    def _route_to_commands(self, route):

        """
        from the shortest path graph, transform it into a list of commands

        :param route: the sub graph containing the shortest path
        :return: list of commands encoded from 0-5
        """

