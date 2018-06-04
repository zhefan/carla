import random


from carla.planner import Planner
from carla.client import make_carla_client
from carla.settings import CarlaSettings

def main():

    planner = Planner(city_name='Town01') #TODO: this will receive a city description

    with make_carla_client('localhost', 2000) as client:

        scene = client.load_settings(CarlaSettings())

        number_of_player_starts = len(scene.player_start_spots)
        player_start = random.randint(0, max(0, number_of_player_starts - 1))

        client.start_episode(player_start)


        route = planner.compute_route(start_transform, end_transform)

        route.waypoints()
        route.commands()




if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
