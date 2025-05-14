import tkinter as tk
import random

class ControlAgentGUI:
    def __init__(self, root, rows=4, cols=4, dirt_regen_prob=0.2, max_energy=6):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.dirt_regen_prob = dirt_regen_prob
        self.max_energy = max_energy
        self.running = False
        self.agent_pos = [0, 0]
        self.charging_station = [rows - 1, cols - 1]  # bottom-right corner
        #self.agent_pos = [initial_x, initial_y]  # Example: [2, 2]
        #self.charging_station = [0, 0]  # Or wherever the station is
        self.setup_simulation()
        self.create_widgets()
        self.update_display()

    def path_to_charging_station(self):
        ax, ay = self.agent_pos
        cx, cy = self.charging_station

        # Move the agent one step closer to the charging station
        if ax < cx:
            ax += 1
        elif ax > cx:
            ax -= 1
        elif ay < cy:
            ay += 1
        elif ay > cy:
            ay -= 1

        self.agent_pos = [ax, ay]

    def setup_simulation(self):
        self.energy = self.max_energy
        self.agent_pos = [0, 0]
        self.charging_station = [self.rows - 1, self.cols - 1]
        self.recharging = False

        self.rooms = [[{'status': 'Dirty', 'dirt_count': 1} for _ in range(self.cols)] for _ in range(self.rows)]
        self.cleaned_rooms = 0
        self.total_dirt_regens = 0
        self.total_energy_used = 0

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=650, height=550)
        self.canvas.pack()

        self.status_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.status_label.pack()

        self.stats_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.stats_label.pack()

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_simulation)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_simulation)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_simulation)
        self.reset_button.pack(side=tk.LEFT, padx=10)

    def update_display(self):
        self.canvas.delete("all")
        room_w, room_h = 130, 100
        pad = 10

        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * (room_w + pad) + pad
                y1 = i * (room_h + pad) + pad
                x2 = x1 + room_w
                y2 = y1 + room_h
                room = self.rooms[i][j]

                if [i, j] == self.charging_station:
                    color = "orange"
                else:
                    color = "green" if room['status'] == 'Clean' else 'brown'

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                if [i, j] == self.agent_pos:
                    self.canvas.create_oval(x1 + 30, y1 + 30, x2 - 30, y2 - 30, fill='blue')

        self.status_label.config(text=f"Energy: {self.energy} | Agent at {self.agent_pos}")
        self.stats_label.config(
            text=f"🧼 Cleaned: {self.cleaned_rooms} | 🔁 Regens: {self.total_dirt_regens} | ⚡ Used: {self.total_energy_used}"
        )

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.run_step()

    def stop_simulation(self):
        self.running = False

    def reset_simulation(self):
        self.running = False
        self.setup_simulation()
        self.update_display()

    def run_step(self):
        if not self.running:
            return

        i, j = self.agent_pos
        room = self.rooms[i][j]

        if self.energy == 0 and not self.recharging:
            self.recharging = True
            self.path_to_charging_station()
            return

        if self.recharging:
            if self.agent_pos == self.charging_station:
                self.status_label.config(text="🔋 Charging...")
                self.root.after(1500, self.recharge)
                return
            else:
                self.move_one_step_toward(self.charging_station)
        else:
            if room['status'] == 'Dirty':
                room['status'] = 'Clean'
                self.cleaned_rooms += 1
                self.energy -= 1
                self.total_energy_used += 1
            else:
                self.energy -= 1
                self.total_energy_used += 1
                self.move_to_next_room()

        self.regenerate_dirt()
        self.update_display()
        self.root.after(700, self.run_step)

    def move_to_next_room(self):
        i, j = self.agent_pos
        idx = i * self.cols + j
        next_idx = (idx + 1) % (self.rows * self.cols)
        self.agent_pos = [next_idx // self.cols, next_idx % self.cols]

    def move_one_step_toward(self, target):
        ai, aj = self.agent_pos
        ti, tj = target

        if ai < ti:
            ai += 1
        elif ai > ti:
            ai -= 1
        elif aj < tj:
            aj += 1
        elif aj > tj:
            aj -= 1

        self.agent_pos = [ai, aj]

    def recharge(self):
        self.energy = self.max_energy
        self.recharging = False
        self.status_label.config(text="✅ Recharged!")
        self.run_step()

    def regenerate_dirt(self):
        for i in range(self.rows):
            for j in range(self.cols):
                room = self.rooms[i][j]
                if room['status'] == 'Clean' and random.random() < self.dirt_regen_prob:
                    room['status'] = 'Dirty'
                    room['dirt_count'] += 1
                    self.total_dirt_regens += 1

# Start the GUI
root = tk.Tk()
root.title("AI Cleaning Agent with Stop & Reset")
app = ControlAgentGUI(root)
root.mainloop()
