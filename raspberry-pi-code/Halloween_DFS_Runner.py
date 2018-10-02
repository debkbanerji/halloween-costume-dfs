import time
import RPi.GPIO as GPIO  # Import GPIO library

print('RUNNING DFS LED SCRIPT')

start_button_pin_number = 2
stop_button_pin_number = 3 

pin_number_map = {
    'A': 17
}

adjacency_list = {
    'A': []
}

start_node = 'A'

delay_seconds = 1
flash_seconds = 0.2

GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering
GPIO.setup(start_button_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_button_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

algorithm_currently_running = False

for node in pin_number_map.keys():
    GPIO.setup(pin_number_map[node], GPIO.OUT)


def start_dfs():
    # print('Starting DFS')
    reset_system()
    global algorithm_currently_running
    algorithm_currently_running = True
    dfs(start_node, [])
    
    # Flash grapgh once done
    for i in range(0, 3):
        time.sleep(flash_seconds)
        turn_on_all_leds()
        time.sleep(flash_seconds)
        turn_off_all_leds()

    reset_system()
    algorithm_currently_running = False
    # print('Ending DFS')

def dfs(node, visited_list):
    global algorithm_currently_running
    if algorithm_currently_running and should_stop():  # don't check GPIO if we don't have to
        algorithm_currently_running = False
        reset_system()
    if node not in visited_list and algorithm_currently_running:
        visited_list.append(node)
        # print('highlight')
        highlight_node(node)
        time.sleep(delay_seconds)
        for adjacent_node in adjacency_list[node]:
            dfs(adjacent_node, visited_list)


def highlight_node(node):
    turn_on_led(pin_number_map[node])


def turn_off_led(pin_number):
    GPIO.output(pin_number, GPIO.LOW)
    # print('TURNING OFF ' + str(pin_number))


def turn_on_led(pin_number):
    GPIO.output(pin_number, GPIO.HIGH)
    # print('TURNING ON ' + str(pin_number))


def turn_off_all_leds():
    for node in pin_number_map.keys():
        turn_off_led(pin_number_map[node])


def turn_on_all_leds():
    for node in pin_number_map.keys():
        turn_on_led(pin_number_map[node])


def reset_system():
    global algorithm_currently_running
    algorithm_currently_running = False
    turn_off_all_leds()


def should_start():
    input_state = GPIO.input(start_button_pin_number)
    return not input_state


def should_stop():
    input_state = GPIO.input(stop_button_pin_number)
    return not input_state


# Main runner
reset_system()
while True:
    #print(GPIO.input(start_button_pin_number))
    #print(GPIO.input(stop_button_pin_number))
    time.sleep(flash_seconds)
    if not algorithm_currently_running and should_start():
        start_dfs()
