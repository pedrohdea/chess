from numpy import array
from engine.predict import get_command

command = "a8b3"
ALFABHETIC = ["a", "b", "c", "d", "e", "f", "g", "h"]

led_to_pop = ALFABHETIC.index(command[0]), int(command[1]) - 1
led_to_top = ALFABHETIC.index(command[2]), int(command[3]) - 1

modify_frame = start_matrix = array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
)

command = get_command(modify_frame)
assert command=='a7a6'