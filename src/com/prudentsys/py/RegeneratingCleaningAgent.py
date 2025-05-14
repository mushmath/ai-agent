import random
import time

class RegeneratingCleaningAgent:
    def __init__(self, rooms, dirt_regen_prob=0.2, max_steps=20):
        self.rooms = rooms
        self.environment = {room: 'Dirty' for room in rooms}
        self.current_room_index = 0
        self.dirt_regen_prob = dirt_regen_prob
        self.max_steps = max_steps

    def perceive(self):
        current_room = self.rooms[self.current_room_index]
        status = self.environment[current_room]
        return current_room, status

    def act(self, perception):
        room, status = perception
        if status == 'Dirty':
            print(f"[Agent] Room {room} is dirty. Cleaning...")
            self.environment[room] = 'Clean'
        else:
            print(f"[Agent] Room {room} is clean. Moving on.")

        self.move_to_next_room()

    def move_to_next_room(self):
        self.current_room_index = (self.current_room_index + 1) % len(self.rooms)

    def regenerate_dirt(self):
        for room in self.rooms:
            if self.environment[room] == 'Clean' and random.random() < self.dirt_regen_prob:
                self.environment[room] = 'Dirty'
                print(f"[Environment] Room {room} became dirty again!")

    def run(self):
        for step in range(1, self.max_steps + 1):
            print(f"\n🔄 Step {step}")
            self.regenerate_dirt()
            perception = self.perceive()
            self.act(perception)
            time.sleep(0.5)  # Delay to simulate real-time operation

        print("\n⏹️ Stopping agent after max steps.")
        print(f"Final environment state: {self.environment}")

# Run the agent
agent = RegeneratingCleaningAgent(['A', 'B', 'C', 'D'], dirt_regen_prob=0.3, max_steps=30)
agent.run()
