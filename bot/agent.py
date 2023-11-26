import math
from lux.game import Game
from lux.game_map import Cell
from lux.constants import Constants

DIRECTIONS = Constants.DIRECTIONS
game_state = None


class Agent:
    """
    Base agent for handling game state and coordinating units/cities.

    This class houses 3 child classes:
    - Worker
    - Cart
    - City

    These implement their own Q-tables (?) and reward functions to dictate their moves.

    Should these should run as separate models, training individually
    """

    def __init__(self, *, observation):
        self.game_state = Game()
        self.game_state._initialize(observation.updates)
        self.game_state._update(observation.updates[2:])
        self.game_state.id = observation.player

    def update(self, *, observation):
        """
        Update the game state with another observation.
        """
        self.game_state._update(observation.updates)

    def get_actions(self, observation):
        """
        For the given game_state, produce a set of actions for all the units/cities.
        """
        actions = []
        player = self.game_state.players[observation.player]
        #  opponent = self.game_state.players[(observation.player + 1) % 2]
        width, height = self.game_state.map.width, self.game_state.map.height

        resource_tiles: list[Cell] = []
        for y in range(height):
            for x in range(width):
                cell = self.game_state.map.get_cell(x, y)
                if cell.has_resource():
                    resource_tiles.append(cell)

        # we iterate over all our units and do something with them
        for unit in player.units:
            if unit.is_worker() and unit.can_act():
                closest_dist = math.inf
                closest_resource_tile = None
                if unit.get_cargo_space_left() > 0:
                    # if the unit is a worker and we have space in cargo, lets
                    # find the nearest resource tile and try to mine it
                    for resource_tile in resource_tiles:
                        if (
                            resource_tile.resource.type == Constants.RESOURCE_TYPES.COAL
                            and not player.researched_coal()
                        ):
                            continue
                        if (
                            resource_tile.resource.type
                            == Constants.RESOURCE_TYPES.URANIUM
                            and not player.researched_uranium()
                        ):
                            continue
                        dist = resource_tile.pos.distance_to(unit.pos)
                        if dist < closest_dist:
                            closest_dist = dist
                            closest_resource_tile = resource_tile
                    if closest_resource_tile is not None:
                        actions.append(
                            unit.move(unit.pos.direction_to(closest_resource_tile.pos))
                        )
                else:
                    # if unit is a worker and there is no cargo space left, and
                    # we have cities, lets return to them
                    if len(player.cities) > 0:
                        closest_dist = math.inf
                        closest_city_tile = None
                        for k, city in player.cities.items():
                            for city_tile in city.citytiles:
                                dist = city_tile.pos.distance_to(unit.pos)
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_city_tile = city_tile
                        if closest_city_tile is not None:
                            move_dir = unit.pos.direction_to(closest_city_tile.pos)
                            actions.append(unit.move(move_dir))
        return actions


class Worker:
    pass


class Cart:
    pass


class City:
    pass
