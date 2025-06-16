ALFABHETIC = ["a", "b", "c", "d", "e", "f", "g", "h"]


def get_vector(move):
    move = "a8a6"
    if len(move) != 4:
        raise

    last_pos = ALFABHETIC.index(move[0]), int(move[1])
    new_pos = ALFABHETIC.index(move[2]), int(move[3])

    return last_pos, new_pos


def turn_on_leds(move):
    last_pos, new_pos = get_vector(move)
    ## liga led
