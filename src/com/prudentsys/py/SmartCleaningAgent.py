class SmartCleaningAgent:
    def __init__(self, rooms):
        self.rooms = rooms
        self.environment = {room: 'Dirty' for room in rooms}
        self.cleaned_rooms = set()
        self.current_room_index = 0

    def perceive(self):
        current_room = self.rooms[self.current_room_index]
        status = self.environment[current_room]
        return current_room, status

    def act(self, perception):
        room, status = perception
        if status == 'Dirty':
            print(f"Room {room} is dirty. Cleaning...")
            self.environment[room] = 'Clean'
            self.cleaned_rooms.add(room)
        else:
            print(f"Room {room} is already clean.")

        # Move to the next dirty room, if any
        self.move_to_next_dirty_room()

    def move_to_next_dirty_room(self):
        for i in range(len(self.rooms)):
            next_index = (self.current_room_index + i + 1) % len(self.rooms)
            if self.environment[self.rooms[next_index]] == 'Dirty':
                self.current_room_index = next_index
                return
        # All rooms are clean
        self.current_room_index = None

    def run(self):
        steps = 0
        while 'Dirty' in self.environment.values():
            perception = self.perceive()
            self.act(perception)
            steps += 1
            if self.current_room_index is None:
                break
        print("\n✅ All rooms are clean.")
        print(f"Final environment state: {self.environment}")
        print(f"Total steps taken: {steps}")

# Example with 4 rooms
agent = SmartCleaningAgent(['A', 'B', 'C', 'D'])
agent.run()
