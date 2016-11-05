from hlt import *
from networking import *
import numpy
# import logging
# logging.basicConfig(filename='last_run.log', level=logging.INFO)

myID, gameMap = getInit()
sendInit("de846Bot")


while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            #leave the above alone
            # xy_owner = gameMap.getSite(Location(x, y)).owner
            # xy_strength = gameMap.getSite(Location(x, y)).strength
            # xy_production = gameMap.getSite(Location(x, y)).production
            # logging.info("coord:{}, {}".format(x, y))
            # logging.info("owner:{}".format(xy_owner))
            # logging.info("strength:{}".format(xy_strength))
            # logging.info("production :{}".format(xy_production))

            if gameMap.getSite(Location(x, y)).owner == myID:
                movedPiece = False
                if y <= 10:
                    moves.append(Move(Location(x,y), STILL))
                    movedPiece = True
                if not movedPiece and y <= 30:
                    for d in CARDINALS:
                        if gameMap.getSite(Location(x,y), d).owner != myID:
                            if gameMap.getSite(Location(x,y), d).strength > \
                                            3 * gameMap.getSite(Location(x,y)).strength:
                                moves.append(Move(Location(x,y), STILL))
                                movedPiece = True
                if not movedPiece:
                    for d in CARDINALS:
                        if gameMap.getSite(Location(x,y), d).owner != myID and \
                                        gameMap.getSite(Location(x,y), d).strength < gameMap.getSite(Location(x,y)).strength:
                            moves.append(Move(Location(x,y), d))
                            movedPiece = True
                            break
                if not movedPiece and gameMap.getSite(Location(x, y)).strength < gameMap.getSite(Location(x,y)).production * 2:
                    moves.append(Move(Location(x,y), STILL))
                    movedPiece = True
                if not movedPiece:
                    moves.append(Move(Location(x,y), NORTH if bool(int(random.random() * 2)) else WEST))
                    movedPiece = True
    sendFrame(moves)
