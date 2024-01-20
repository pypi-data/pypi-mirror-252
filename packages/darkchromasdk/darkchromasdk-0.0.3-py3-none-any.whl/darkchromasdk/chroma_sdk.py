import threading
from time import sleep
import requests
import keyboard
import json
from color_parsing import parse_rgb
from pynput.mouse import Listener

global middle_mouse_pressed


# Callback function for mouse events
def on_click(_, __, button, pressed):
    global middle_mouse_pressed
    if button == button.middle:
        middle_mouse_pressed = pressed


def heartbeat_thread(chromasdk):
    try:
        while True:
            if chromasdk.enabled:
                requests.put(chromasdk.uri + '/heartbeat')
                sleep(1)
            else:
                break
    except KeyboardInterrupt:
        print("KeyboardInterrupt, exiting...")
        chromasdk.quit()
        exit(0)


class ChromaSDK:
    def __init__(self, config_path):
        """
        Initialize the Chroma SDK
        :param config_path: the path to the config json file
        """
        self.config_path = config_path
        self.config = json.load(open(config_path))
        self.map = self.config['map']

        self.id, self.uri = self._initialize()

        self.enabled = True
        self.heartbeat_thread = threading.Thread(target=heartbeat_thread, args=(self,))
        self.heartbeat_thread.start()

        sleep(3)

    def _initialize(self):
        """
        used to initialize the Chroma SDK
        :return:
        """
        # send config to server, and get session id
        response = requests.post('http://localhost:54235/razer/chromasdk', json=self.config['chroma'])
        print(f"response from init: {response.json()}")
        try:
            return response.json()['sessionid'], response.json()['uri']
        except KeyError:
            raise Exception("Error while initializing Chroma SDK")

    def save_config(self):
        """
        Save the config to the config file
        :return:
        """
        json.dump(self.config, open(self.config_path, 'w'), indent=4)

    def quit(self):
        """
        Quit the Chroma SDK
        :return:
        """
        requests.delete(self.uri)
        self.enabled = False
        self.heartbeat_thread.join()

    def send_grid(self, grid):
        """
        Send a grid of color values to the api (6 rows, 22 columns)
        :param grid: an array of rows of color values (NOT RGB, use parse_rgb in color_parsing.py)
        :return:
        """
        data = {
            'effect': 'CHROMA_CUSTOM',
            'param': grid
        }
        try:
            requests.put(self.uri + '/keyboard', json=data)
        except requests.exceptions.ConnectionError:
            print("ConnectionError while sending grid...")
            sleep(2)

    def light_index(self, pos, color):
        """
        used to only light up one key
        :param pos: the position in the array (x, y)
        :param color: the color to light up the key (rgb)
        :return:
        """
        parsed_color = parse_rgb(color)

        # generate array with 6 rows and 22 columns of 0
        grid = [[0 for _ in range(22)] for _ in range(6)]

        # set the color of the key
        grid[pos[1]][pos[0]] = parsed_color

        # send the array to the server
        self.send_grid(grid)

    def light_static(self, color):
        """
        light up the entire keyboard with one color
        :param color: the color to light up the keyboard (rgb)
        :return:
        """
        color = parse_rgb(color)
        data = {
            "effect": "CHROMA_STATIC",
            "param": {
                "color": color
            }
        }
        requests.put(self.uri + '/keyboard', json=data)

    def light_keys(self, keys, color=(0, 0, 0), background=(0, 0, 0)):
        """
        light up multiple keys
        :param keys: a dict of keys and colors or a list of keys
        :param color: if keys is a list, this is the color to light up the keys (rgb)
        :param background: the background color (rgb)
        :return:
        """
        multi_color = isinstance(keys, dict)
        if multi_color:
            corrected_keys = []
            corrected_colors = []

            for key in keys:
                corrected_keys.append(key)
                corrected_colors.append(keys[key])

            keys = corrected_keys

        positions = [self.map[key] for key in keys if key in self.map]

        # generate array with 6 rows and 22 columns of 0
        grid = [[parse_rgb(background) for _ in range(22)] for _ in range(6)]

        # set the color of the keys
        for pos in positions:
            if multi_color:
                grid[pos[0]][pos[1]] = parse_rgb(corrected_colors[positions.index(pos)])
            else:
                grid[pos[0]][pos[1]] = parse_rgb(color)

        self.send_grid(grid)

    def generate_map(self):
        """
        used to generate the map of keys to positions
        :return:
        """
        self.light_static((0, 0, 0))

        saved_keys = []
        for row in range(6):
            for key_index in range(22):
                self.light_index((key_index, row), (0, 0, 255))

                print("press lit up key or alt n to skip")
                while True:
                    event = keyboard.read_event()

                    if event.is_keypad:
                        event.name = "keypad " + event.name
                    event.name = event.name.replace(" ", "_")

                    if event.name not in saved_keys:
                        break
                    else:
                        print("key already saved")

                    if middle_mouse_pressed:
                        print("skipped")
                        sleep(.5)
                        break

                if middle_mouse_pressed:
                    print("skipped")
                    sleep(.5)
                    continue

                self.map[event.name.lower()] = [row, key_index]

                print(f"key {event.name.lower()} saved")
                saved_keys.append(event.name.lower())

                sleep(.2)

        self.save_config()


listener = Listener(on_click=on_click)
listener.start()
