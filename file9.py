import tkinter as tk
import time
import threading


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
            print(f"Mode set to: {self.mode}")  # Debug print
        else:
            self.next_mode = mode  # Set next_mode to switch after current cycle
            print(f"Next mode set to: {self.next_mode}")  # Debug print

    def start(self):
        self.running = True
        threading.Thread(target=self.run).start()

    def stop(self):
        self.running = False
        if self.flashing_thread is not None:
            self.flashing_thread.join()  # Wait for the flashing thread to finish

    def run(self):
        while self.running:
            print(f"Current mode: {self.mode}")  # Debug print
            if self.mode == 5:
                self.flash_lights()
            elif self.mode == 2:
                self.red_light_mode()
            elif self.mode in [3, 4]:
                self.green_light_mode()
            else:
                self.traffic_cycle()

            # If there is a next mode set, switch to it
            if self.next_mode is not None:
                print(f"Switching to next mode: {self.next_mode}")  # Debug print
                self.mode = self.next_mode
                self.next_mode = None

    def traffic_cycle(self):
        for i in range(2):  # For two sets of traffic lights
            self.current_light[i] = 2  # Green
            print(f"Set light {i} to Green")  # Debug print
            self.update_lights()
            time.sleep(3)  # Green for 3 seconds

            self.current_light[i] = 1  # Yellow
            print(f"Set light {i} to Yellow")  # Debug print
            self.update_lights()
            time.sleep(1)  # Yellow for 1 second

            self.current_light[i] = 0  # Red
            print(f"Set light {i} to Red")  # Debug print
            self.update_lights()
            time.sleep(1)  # Red for 1 second

            # Set the other light to Red
            self.current_light[1 - i] = 0  # Ensure the other light is Red
            self.update_lights()

    def flash_lights(self):
        self.flashing_thread = threading.current_thread()  # Set the current thread for flashing
        while self.running and self.mode == 5:
            for i in range(2):
                self.current_light[i] = 0  # Red
                print(f"Flashing light {i}: Red")  # Debug print
            self.update_lights()
            time.sleep(0.5)

            for i in range(2):
                self.current_light[i] = 3  # Off (keeping it red)
                print(f"Flashing light {i}: Off")  # Debug print
            self.update_lights()
            time.sleep(0.5)

            # Check if mode has changed
            if self.next_mode is not None:
                print(f"Switching to next mode: {self.next_mode} from flash_lights")  # Debug print
                self.mode = self.next_mode
                self.next_mode = None
                break  # Exit the loop to allow switching

    def red_light_mode(self):
        print("Mode 2: LUMIERE ROUGE, LES PIETONS PEUVENT PASSER")  # Debug print
        for i in range(2):
            self.current_light[i] = 0  # Red
            self.update_lights()
        time.sleep(10)  # Stay red for 10 seconds
        self.next_mode = 1  # Return to mode 1 after

    def green_light_mode(self):
        if self.mode == 3:
            print("Mode 3: Light 0 Green")  # Debug print
            self.current_light = [2, 0]  # Set light 0 to Green, light 1 to Red
        elif self.mode == 4:
            print("Mode 4: Light 1 Green")  # Debug print
            self.current_light = [0, 2]  # Set light 0 to Red, light 1 to Green

        self.update_lights()
        time.sleep(5)  # Stay in the green mode for 5 seconds
        self.next_mode = 1  # Return to mode 1 after

    def update_lights(self):
        for i in range(2):
            # Clear previous lights
            self.canvas.itemconfig(self.light_positions[i][0], fill='gray')  # Red
            self.canvas.itemconfig(self.light_positions[i][1], fill='gray')  # Yellow
            self.canvas.itemconfig(self.light_positions[i][2], fill='gray')  # Green

            # Set the current lights
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

        # Define the light positions
        self.light_positions = [
            [self.canvas.create_oval(50, 50, 100, 100, fill='gray'),  # Set 1 Red
             self.canvas.create_oval(50, 110, 100, 160, fill='gray'),  # Set 1 Yellow
             self.canvas.create_oval(50, 170, 100, 220, fill='gray')],  # Set 1 Green
            [self.canvas.create_oval(250, 50, 300, 100, fill='gray'),  # Set 2 Red
             self.canvas.create_oval(250, 110, 300, 160, fill='gray'),  # Set 2 Yellow
             self.canvas.create_oval(250, 170, 300, 220, fill='gray')]  # Set 2 Green
        ]

        self.traffic_light = TrafficLight(self.canvas, self.light_positions)

        # Create buttons for modes
        self.start_button = tk.Button(root, text="Mode 1", command=lambda: self.set_mode(1))
        self.start_button.pack()

        self.mode2_button = tk.Button(root, text="Mode 2", command=lambda: self.set_mode(2))
        self.mode2_button.pack()

        self.mode3_button = tk.Button(root, text="Mode 3", command=lambda: self.set_mode(3))
        self.mode3_button.pack()

        self.mode4_button = tk.Button(root, text="Mode 4", command=lambda: self.set_mode(4))
        self.mode4_button.pack()

        self.mode5_button = tk.Button(root, text="Mode 5 (Flash)", command=lambda: self.set_mode(5))
        self.mode5_button.pack()

        self.start_traffic_light()

    def set_mode(self, mode):
        self.traffic_light.set_mode(mode)

    def start_traffic_light(self):
        self.traffic_light.start()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Traffic Light Control")
    app = TrafficLightApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.traffic_light.stop(), root.destroy()))
    root.mainloop()
