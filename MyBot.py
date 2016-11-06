from hlt import *
from networking import *
# import numpy as np
# import itertools
# import logging
# logging.basicConfig(filename='lastrun.log', filemode='w', level=logging.INFO)

myID, gameMap = getInit()
sendInit("de846Bot")


#TODO pieces that are closer to the edge should prefer to move closer towards edges
#TODO if piece is full strength, move to unowned block instead of just moving south or west

while True:
    moves = []
    gameMap = getFrame()

    # figure out how far we are from game border
    hilomap = {'lo_x': None, 'hi_x': None, 'lo_y': None, 'hi_y': None}
    x_seen = {x: None for x in range(gameMap.width)}
    y_seen = {y: None for y in range(gameMap.width)}

    # localGameMap = np.empty((gameMap.width, gameMap.height), dtype=dict)
    # strength_map = np.zeros((gameMap.width, gameMap.height), dtype=np.int32)
    # production_map = np.zeros((gameMap.width, gameMap.height), dtype=np.int32)
    # owner_map = np.zeros((gameMap.width, gameMap.height), dtype=np.int32)

    for y in range(gameMap.height):
        for x in range(gameMap.width):
            this_loc = gameMap.getSite(Location(x, y))
            this_str = this_loc.strength
            this_prod = this_loc.production
            this_owner = this_loc.owner
            # strength_map[y,x] = this_loc.strength
            # production_map[y,x] = this_loc.production
            # owner_map[y,x] = this_loc.owner

            if hilomap['lo_x'] is not None:
                if this_owner == myID and x < hilomap['lo_x']:
                    hilomap['lo_x'] = x
            elif this_owner == myID:
                hilomap['lo_x'] = x

            if hilomap['hi_x'] is not None:
                if this_owner == myID and x > hilomap['hi_x']:
                    hilomap['hi_x'] = x
            elif this_owner == myID:
                hilomap['hi_x'] = x

            if hilomap['lo_y'] is not None:
                if this_owner == myID and y < hilomap['lo_y']:
                    hilomap['lo_y'] = y
            elif this_owner == myID:
                hilomap['lo_y'] = y

            if hilomap['hi_y'] is not None:
                if this_owner == myID and y > hilomap['hi_y']:
                    hilomap['hi_y'] = y
            elif this_owner == myID:
                hilomap['hi_y'] = y

            # localGameMap[y, x] =  {"strength": this_loc.strength, "production": this_loc.production, "owner": this_loc.owner}

    # begin our own loop of each game piece
    # for y, x in itertools.product(range(owner_map.shape[0]), range(owner_map.shape[1])):

            if this_owner == myID:
                movedPiece = False

                # Territory Expansion
                if not movedPiece:
                    if hilomap['hi_y'] - hilomap['lo_y'] == hilomap['hi_x'] - hilomap['lo_x'] and this_str >= 250:
                        moves.append(Move(Location(x, y), int(random.random() * 5)))
                        movedPiece = True

                if not movedPiece:
                    if hilomap['hi_y'] - hilomap['lo_y'] > hilomap['hi_x'] - hilomap['lo_x'] and this_str >= 240:
                        if hilomap['lo_x'] - x <= 1:
                            moves.append(Move(Location(x, y), WEST))
                            movedPiece = True
                        elif hilomap['hi_x'] - x <= 1:
                            moves.append(Move(Location(x, y), EAST))
                            movedPiece = True
                    else:
                        if hilomap['lo_y'] - y <= 1:
                            moves.append(Move(Location(x,y), NORTH))
                            movedPiece = True
                        elif hilomap['hi_y'] - y <= 1:
                            moves.append(Move(Location(x,y), SOUTH))
                            movedPiece = True

                if not movedPiece:
                    for d in CARDINALS:
                        if gameMap.getSite(Location(x,y), d).owner != myID and \
                                        gameMap.getSite(Location(x,y), d).strength < this_str:
                            moves.append(Move(Location(x,y), d))
                            movedPiece = True
                            break

                # if not movedPiece and gameMap.getSite(Location(x, y)).strength > 82:
                #     if (int(random.random()) * 10) % 10 < 7:
                #         moves.append(Move(Location(x,y), SOUTH))
                #     else:
                #         moves.append(Move(Location(x,y), WEST))
                #     movedPiece = True

                if not movedPiece:
                    for d in CARDINALS:
                       if gameMap.getSite(Location(x,y), d).production >= 2 * gameMap.getSite(Location(x,y)).production:
                            moves.append(Move(Location(x,y), d))
                            movedPiece = True
                            break

                if not movedPiece and gameMap.getSite(Location(x,y)).strength < gameMap.getSite(Location(x,y)).production * 3:
                    moves.append(Move(Location(x,y), STILL))
                    movedPiece = True

                if not movedPiece:
                    moves.append(Move(Location(x,y), STILL))
                    movedPiece = True


    # logging.info('strength: {}'.format(strength_map))
    # logging.info('owner: {}'.format(owner_map))
    # logging.info('hilomap: {}'.format(hilomap))
    # logging.info(localGameMap)
    sendFrame(moves)
