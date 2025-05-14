class SimpleCleaningAgent:
    def __init__(self):
        self.location = 'A'  # Start in room A
        self.environment = {'A': 'Dirty', 'B': 'Dirty'}  # Initial state

    def perceive(self):
        return self.location, self.environment[self.location]

    def act(self, perception):
        location, status = perception
        if status == 'Dirty':
            print(f"Room {location} is dirty. Cleaning...")
            self.environment[location] = 'Clean'
        else:
            print(f"Room {location} is clean. Moving to the other room.")
            self.location = 'B' if location == 'A' else 'A'

    def run(self):
        steps = 0
        while 'Dirty' in self.environment.values():
            perception = self.perceive()
            self.act(perception)
            steps += 1
        print("\nAll rooms are clean.")
        print(f"Final environment state: {self.environment}")
        print(f"Total steps taken: {steps}")

# Run the agent
agent = SimpleCleaningAgent()
agent.run()
