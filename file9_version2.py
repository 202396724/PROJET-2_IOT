import tkinter as tk
import time
import threading
import paho.mqtt.client as mqtt

class TrafficLight:
    def __init__(self, canvas, light_positions):
        self.mode = 1
        self.running = False
        self.canvas = canvas
        self.light_positions = light_positions
        self.current_light = [0, 0]  # 0: Red, 1: Yellow, 2: Green
        self.next_mode = None  # Store the next mode to switch to
        self.flashing_thread = None  # Keep track of the flashing thread

    def set_mode(self, mode):
        if not self.running:
            self.mode = mode
        else:
            self.next_mode = mode

    def start(self):
        self.running = True
        threading.Thread(target=self.run).start()

    def stop(self):
        self.running = False
        if self.flashing_thread is not None:
            self.flashing_thread.join()  # Wait for the flashing thread to finish

    def run(self):
        while self.running:
            if self.mode == 5:
                self.flash_lights()
            elif self.mode == 2:
                self.red_light_mode()
            elif self.mode in [3, 4]:
                self.green_light_mode()
            else:
                self.traffic_cycle()

            if self.next_mode is not None:
                self.mode = self.next_mode
                self.next_mode = None

    def traffic_cycle(self):
        for i in range(2):
            self.current_light[i] = 2  # Green
            self.update_lights()
            time.sleep(3)  # Green for 3 seconds
            self.current_light[i] = 1  # Yellow
            self.update_lights()
            time.sleep(1)
            self.current_light[i] = 0  # Red
            self.update_lights()
            time.sleep(1)

    def flash_lights(self):
        self.flashing_thread = threading.current_thread()
        while self.running and self.mode == 5:
            for i in range(2):
                self.current_light[i] = 0  # Red
            self.update_lights()
            time.sleep(0.5)
            for i in range(2):
                self.current_light[i] = 3  # Off
            self.update_lights()
            time.sleep(0.5)

    def red_light_mode(self):
        for i in range(2):
            self.current_light[i] = 0  # Red
        self.update_lights()
        time.sleep(10)
        self.next_mode = 1  # Return to mode 1 after

    def green_light_mode(self):
        if self.mode == 3:
            self.current_light = [2, 0]  # Set light 0 to Green, light 1 to Red
        elif self.mode == 4:
            self.current_light = [0, 2]  # Set light 0 to Red, light 1 to Green
        self.update_lights()
        time.sleep(5)
        self.next_mode = 1

    def update_lights(self):
        for i in range(2):
            self.canvas.itemconfig(self.light_positions[i][0], fill='gray')
            self.canvas.itemconfig(self.light_positions[i][1], fill='gray')
            self.canvas.itemconfig(self.light_positions[i][2], fill='gray')

            if self.current_light[i] == 0:
                self.canvas.itemconfig(self.light_positions[i][0], fill='red')
            elif self.current_light[i] == 1:
                self.canvas.itemconfig(self.light_positions[i][1], fill='yellow')
            elif self.current_light[i] == 2:
                self.canvas.itemconfig(self.light_positions[i][2], fill='green')


class TrafficLightApp:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=400, height=300)
        self.canvas.pack()
        self.light_positions = [
            [self.canvas.create_oval(50, 50, 100, 100, fill='gray'),
             self.canvas.create_oval(50, 110, 100, 160, fill='gray'),
             self.canvas.create_oval(50, 170, 100, 220, fill='gray')],
            [self.canvas.create_oval(250, 50, 300, 100, fill='gray'),
             self.canvas.create_oval(250, 110, 300, 160, fill='gray'),
             self.canvas.create_oval(250, 170, 300, 220, fill='gray')]
        ]
        self.traffic_light = TrafficLight(self.canvas, self.light_positions)
        self.start_traffic_light()

        # Start MQTT subscriber
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect('localhost', 1883)
        self.mqtt_client.subscribe('traffic_light/mode')
        self.mqtt_client.loop_start()

    def on_message(self, client, userdata, message):
        command = message.payload.decode('utf-8')
        mode = self.map_command_to_mode(command)
        if mode is not None:
            self.traffic_light.set_mode(mode)

    def map_command_to_mode(self, command_text):
        command_mapping = {
            "mode 1": 1,
            "mode 2": 2,
            "mode 3": 3,
            "mode 4": 4,
            "mode 5": 5
        }
        return command_mapping.get(command_text.lower(), None)

    def start_traffic_light(self):
        self.traffic_light.start()


# Main application
root = tk.Tk()
app = TrafficLightApp(root)
root.mainloop()
