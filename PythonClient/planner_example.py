import random


from carla.planner import Planner
from carla.client import make_carla_client
from carla.settings import CarlaSettings

def main():

    planner = Planner(city_name='Town01') #TODO: this will receive a city description

    with make_carla_client('localhost', 2000) as client:



        scene = client.load_settings(CarlaSettings())
        # Set the number of episodes
        number_of_episodes = 30
        for i in range(number_of_episodes):
            print (scene.player_start_spots)
            number_of_player_starts = len(scene.player_start_spots)
            player_start = random.randint(0, max(0, number_of_player_starts - 1))
            start_transform = scene.player_start_spots[player_start]
            player_end = random.randint(0, max(0, number_of_player_starts - 1))
            end_transform = scene.player_start_spots[player_end]


            client.start_episode(player_start)

            # For a given start and end point the planner can compute the route.
            route = planner.compute_route(start_transform, end_transform)
            # Route is a resulting object that could produce derivate representations
            # of the resulting route.

            # For instance, route can be converted into waypoints, that are future positions
            # on the road that the agent should go in order to reach the goal. The parameters for this
            # are the number of waypoints and the distance ( in meters between each waypoints)
            waypoints = route.waypoints(number_of_waypoints=100, waypoint_spacing=1)
            # Also the route can be converted into a set of high level commands such as STRAIGHT,
            # LEFT, RIGHT. For this case we get the next high level command (position 0) that the
            # agent has to use to be guided to the goal.
            next_high_level_command = route.commands()[0]




if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
