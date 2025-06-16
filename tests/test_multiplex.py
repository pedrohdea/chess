import RPi.GPIO as gpio
from pi74HC595 import pi74HC595


def liga_led_x(x, y):
    gpio.setmode(gpio.BOARD)
    shift_register = pi74HC595(daisy_chain=2)
    shift_register.set_by_list([0, 1, 0, 1, 0, 1, 0, 1])
    shift_register.set_by_list([0, 1, 0, 1, 0, 1, 0, 1])


liga_led_x(1, 1)
