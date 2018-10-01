import time
import RPi.GPIO as GPIO  # Import GPIO library

start_button_pin_number = -1  # TODO: SET
stop_button_pin_number = -1  # TODO: SET

pin_number_map = {

}

adjacency_list = {

}

start_node = 'S'

delay_seconds = 1
flash_seconds = 0.4

GPIO.setmode(GPIO.BOARD)  # Set GPIO pin numbering
GPIO.setup(start_button_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_button_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

algorithm_currently_running = True


def start_dfs():
    global algorithm_currently_running
    algorithm_currently_running = True
    reset_system()
    dfs(start_node, [])
    for i in range(0, 2):
        turn_off_all_leds()
        time.sleep(flash_seconds)
        turn_on_all_leds()
    reset_system()
    algorithm_currently_running = False


def dfs(node, visited_list):
    global algorithm_currently_running
    if algorithm_currently_running and should_stop():  # don't check GPIO if we don't have to
        algorithm_currently_running = False
        reset_system()
    if node not in visited_list and algorithm_currently_running:
        visited_list.append(node)
        highlight_node(node)
        time.sleep(delay_seconds)
        for adjacent_node in adjacency_list[node]:
            dfs(adjacent_node, visited_list)


def highlight_node(node):
    turn_on_led(pin_number_map[node])


def turn_off_led(pin_number):
    print('TURNING OFF ' + str(pin_number))


def turn_on_led(pin_number):
    print('TURNING ON ' + str(pin_number))


def turn_off_all_leds():
    for node in pin_number_map.keys():
        turn_off_led(adjacency_list[node])


def turn_on_all_leds():
    for node in pin_number_map.keys():
        turn_on_led(adjacency_list[node])


def reset_system():
    global algorithm_currently_running
    algorithm_currently_running = True
    turn_off_all_leds()


def should_start():
    input_state = GPIO.input(start_button_pin_number)
    return not input_state


def should_stop():
    input_state = GPIO.input(stop_button_pin_number)
    return not input_state


# Main runner
while True:
    if not algorithm_currently_running and should_start():
        start_dfs()
