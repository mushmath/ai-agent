import random
import time

class EnergyAwareCleaningAgent:
    def __init__(self, rooms, dirt_regen_prob=0.3, max_steps=30, max_energy=5):
        self.rooms = rooms
        self.environment = {room: 'Dirty' for room in rooms}
        self.current_room_index = 0
        self.dirt_regen_prob = dirt_regen_prob
        self.max_steps = max_steps
        self.energy = max_energy
        self.max_energy = max_energy

    def perceive(self):
        current_room = self.rooms[self.current_room_index]
        status = self.environment[current_room]
        return current_room, status

    def act(self, perception):
        room, status = perception

        if self.energy == 0:
            print(f"[Agent] ⚡ Out of energy! Recharging...")
            self.recharge()
            return

        if status == 'Dirty':
            print(f"[Agent] 🧼 Room {room} is dirty. Cleaning...")
            self.environment[room] = 'Clean'
        else:
            print(f"[Agent] ✅ Room {room} is clean. Moving on.")

        self.energy -= 1
        self.move_to_next_room()

    def move_to_next_room(self):
        self.current_room_index = (self.current_room_index + 1) % len(self.rooms)

    def recharge(self):
        print("[Agent] 🔋 Recharging to full energy...")
        time.sleep(1)
        self.energy = self.max_energy

    def regenerate_dirt(self):
        for room in self.rooms:
            if self.environment[room] == 'Clean' and random.random() < self.dirt_regen_prob:
                self.environment[room] = 'Dirty'
                print(f"[Environment] ⚠️ Room {room} became dirty again!")

    def run(self):
        for step in range(1, self.max_steps + 1):
            print(f"\n🔄 Step {step} | Energy: {self.energy}")
            self.regenerate_dirt()
            perception = self.perceive()
            self.act(perception)
            time.sleep(0.5)

        print("\n⏹️ Simulation ended.")
        print(f"Final environment: {self.environment}")

# Run the upgraded agent
agent = EnergyAwareCleaningAgent(['A', 'B', 'C', 'D'], dirt_regen_prob=0.3, max_steps=30, max_energy=5)
agent.run()
