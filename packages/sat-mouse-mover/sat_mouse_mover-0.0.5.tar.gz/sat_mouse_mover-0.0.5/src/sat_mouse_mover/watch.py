from time import sleep
import logging
import mouse


logging.basicConfig(level=logging.INFO)

"""The time in seconds to check if the mouse was moved"""
IDLE_TIME = 60

"""The px to move"""
MOVE_SIZE = 100
move_size = 100


def __mouse_moved(current_pos, last_pos) -> bool:
    """Will return True, if the mouse was moved at the defined IDLE TIME """
    logging.debug("check has mouse moved ?")
    return current_pos != last_pos


def __move_mouse(last_pos: tuple[int, int], direction:str) -> tuple[int,int]:
    """This will move the mouse to the given direction """
    logging.debug(f"mouse was not moved for {IDLE_TIME} seconds")

    x, y = last_pos
    x = x-MOVE_SIZE if direction == 'left' else x+MOVE_SIZE

    mouse.move(x, y, True, 0.2)

    logging.debug(f"mouse auto moved")

    return mouse.get_position()


def start():
    try:
        active = False
        current_pos: tuple[int, int]
        last_pos: tuple[int, int]

        logging.info("Start mouse watch")

        current_pos = last_pos =  mouse.get_position()
        next_direction = "left"

        while True:
            current_pos = mouse.get_position()

            moved = __mouse_moved(current_pos, last_pos)
            if not moved and active:
                next_direction = 'left' if next_direction == 'right' else 'right'
                new_x, new_y = __move_mouse(last_pos, next_direction)
                logging.info(f"It seems like, you are not at the desk at the moment, I moved the mouse for you ;-)")
            elif not active:
                logging.info(f"We jsut started the watcher")
            else:
                # mouse was moved, we set the last_pos to the current_pos
                logging.debug("Mouse moved by human")
                last_pos = current_pos

            active = True
            sleep(IDLE_TIME)


    except KeyboardInterrupt as e:
        logging.info("mouse watch stopped")
        exit(1)