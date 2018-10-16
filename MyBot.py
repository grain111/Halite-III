#!/usr/bin/env python3
# Python 3.6
import hlt
from hlt import constants
from hlt.positionals import Direction

import random
import logging

game = hlt.Game()

ship_role = {}

game.ready("BartBot-v2")
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

while True:
    game.update_frame()

    me = game.me
    game_map = game.game_map

    command_queue = []

    for ship in me.get_ships():

        if not ship.id in ship_role:
            ship_role[ship.id] = "exp"
        if ship_role[ship.id] == "ret":
            if ship.position == me.shipyard.position:
                ship_role[ship.id] = "exp"
            else:
                dir = game_map.naive_navigate(ship, me.shipyard.position)
                command_queue.append(ship.move(dir))
                continue
        if ship.halite_amount > constants.MAX_HALITE / 1.5:
            ship_role[ship.id] = "ret"

        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            command_queue.append(
                ship.move(
                    random.choice([ Direction.North, Direction.South, Direction.East, Direction.West ])))
        else:
            command_queue.append(ship.stay_still())

    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:

        command_queue.append(me.shipyard.spawn())

    game.end_turn(command_queue)
