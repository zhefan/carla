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

            # For this start and end point compute the route.
            route = planner.compute_route(start_transform, end_transform)

            # The route object can be used to get more meaningful objects
            # such as waypoints or commands
            route.waypoints()
            route.commands()




if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
