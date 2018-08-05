import math

from .utils import get_vec_dist, get_angle
from carla.planner.map import CarlaMap

class ObstacleAvoidance(object):

    def __init__(self, param, city_name):


        self._node_density = 50.0
        self._pixel_density = 0.1643

        self._map = CarlaMap(city_name, self._pixel_density, self._node_density)
        self.param = param
        # Select WP Number



    def stop_traffic_light(self, location, agent, wp_vector, wp_angle, speed_factor_tl):

        speed_factor_tl_temp = 1

        if agent.traffic_light.state != 0:  # Not green
            x_agent = agent.traffic_light.transform.location.x
            y_agent = agent.traffic_light.transform.location.y
            tl_vector, tl_dist = get_vec_dist(x_agent, y_agent, location.x, location.y)
            # tl_angle = self.get_angle(tl_vector,[ori_x_player,ori_y_player])
            tl_angle = get_angle(tl_vector, wp_vector)
            # print ('Traffic Light: ', tl_vector, tl_dist, tl_angle)

            if (0 < tl_angle < self.param['tl_angle_thres'] / self.param['coast_factor'] and tl_dist < self.param['tl_dist_thres'] * self.param['coast_factor']) or (
                    0 < tl_angle < self.param['tl_angle_thres'] and tl_dist < self.param['tl_dist_thres']) and math.fabs(
                wp_angle) < 0.2:
                speed_factor_tl_temp = tl_dist / (self.param['coast_factor'] * self.param['tl_dist_thres'])

            if (
                    0 < tl_angle < self.param['tl_angle_thres'] * self.param['coast_factor'] and tl_dist < self.param['tl_dist_thres'] / self.param['coast_factor']) and math.fabs(
                wp_angle) < 0.2:
                speed_factor_tl_temp = 0

            if (speed_factor_tl_temp < speed_factor_tl):
                speed_factor_tl = speed_factor_tl_temp

        return speed_factor_tl

    def stop_pedestrian(self, location, agent, wp_vector, speed_factor_p):

        speed_factor_p_temp = 1

        x_agent = agent.pedestrian.transform.location.x
        y_agent = agent.pedestrian.transform.location.y
        p_vector, p_dist = get_vec_dist(x_agent, y_agent, location.x, location.y)
        # p_angle = self.get_angle(p_vector,[ori_x_player,ori_y_player])
        p_angle = get_angle(p_vector, wp_vector)

        # Define flag, if pedestrian is outside the sidewalk ?


        if (math.fabs(
                p_angle) < self.param['p_angle_thres'] / self.param['coast_factor'] and p_dist < self.param['p_dist_thres'] * self.param['coast_factor']) or (
                0 < p_angle < self.param['p_angle_thres'] and p_dist < self.param['p_dist_thres']
            ):

            if self._map.is_point_on_lane([x_agent, y_agent, 38]):
                print("PEDESTRIAN ON LANE ")
                #speed_factor_p_temp = p_dist / (self.param['coast_factor'] * self.param['p_dist_thres'])
                speed_factor_p_temp = 0
                print('Pedestrian: ', p_vector, p_dist, p_angle)

                print(" Resulting speed factor ", speed_factor_p)
                print (" Case 1 ")
            else:
                print ('Pedestrian close not on lane')

        if (math.fabs(
                p_angle) < self.param['p_angle_thres'] * self.param['coast_factor'] and p_dist < self.param['p_dist_thres'] / self.param['coast_factor']):

            if self._map.is_point_on_lane([x_agent, y_agent, 38]):
                print("PEDESTRIAN ON LANE ")
                speed_factor_p_temp = 0
                print('Pedestrian: ', p_vector, p_dist, p_angle)
                print(" Case 2 ")
            else:
                print ('Pedestrian close not on lane')


        if (speed_factor_p_temp < speed_factor_p):
            speed_factor_p = speed_factor_p_temp


        return speed_factor_p

    def stop_vehicle(self, location, agent, wp_vector, speed_factor_v):
        speed_factor_v_temp = 1
        x_agent = agent.vehicle.transform.location.x
        y_agent = agent.vehicle.transform.location.y
        v_vector, v_dist = get_vec_dist(x_agent, y_agent, location.x, location.y)
        # v_angle = self.get_angle(v_vector,[ori_x_player,ori_y_player])
        v_angle = get_angle(v_vector, wp_vector)
        # print ('Vehicle: ', v_vector, v_dist, v_angle)
        # print (v_angle, self.param['v_angle_thres'], self.param['coast_factor'])
        if (
                -0.5 * self.param['v_angle_thres'] / self.param['coast_factor'] < v_angle < self.param['v_angle_thres'] / self.param['coast_factor'] and v_dist < self.param['v_dist_thres'] * self.param['coast_factor']) or (
                -0.5 * self.param['v_angle_thres'] / self.param['coast_factor'] < v_angle < self.param['v_angle_thres'] and v_dist < self.param['v_dist_thres']):
            speed_factor_v_temp = v_dist / (self.param['coast_factor'] * self.param['v_dist_thres'])
        if (
                -0.5 * self.param['v_angle_thres'] * self.param['coast_factor'] < v_angle < self.param['v_angle_thres'] * self.param['coast_factor'] and v_dist < self.param['v_dist_thres'] / self.param['coast_factor']):
            speed_factor_v_temp = 0

        if (speed_factor_v_temp < speed_factor_v):
            speed_factor_v = speed_factor_v_temp

        return speed_factor_v

    def stop_for_agents(self, location, wp_angle, wp_vector, agents):

        speed_factor = 1
        speed_factor_tl = 1
        speed_factor_p = 1
        speed_factor_v = 1

        for agent in agents:

            if agent.HasField('traffic_light') and self.param['stop4TL']:
                speed_factor_tl = self.stop_traffic_light(location, agent, wp_angle,
                                                          wp_vector, speed_factor_tl)
            if agent.HasField('pedestrian') and self.param['stop4P']:
                speed_factor_p = self.stop_pedestrian(location, agent, wp_vector, speed_factor_p)
            if agent.HasField('vehicle') and self.param['stop4V']:
                speed_factor_v = self.stop_vehicle(location, agent, wp_vector, speed_factor_v)

            speed_factor = min(speed_factor_tl, speed_factor_p, speed_factor_v)

        return speed_factor
