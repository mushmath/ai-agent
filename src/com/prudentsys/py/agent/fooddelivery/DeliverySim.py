import random
import os
import time

GRID_SIZE = 6
OBSTACLE_COUNT = 8
MAX_ENERGY = 20
NUM_AGENTS = 2
CUSTOMER_SPAWN_CHANCE = 0.3


class DeliverySim:
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.restaurant = [0, 0]
        self.agents = [self.restaurant.copy() for _ in range(NUM_AGENTS)]
        self.agent_targets = [None for _ in range(NUM_AGENTS)]

        self.customers = []
        self.obstacles = self.spawn_obstacles(OBSTACLE_COUNT)

        self.steps_taken = 0
        self.completed_deliveries = 0
        self.time_step = 0
        self.energy = MAX_ENERGY

    def spawn_obstacles(self, count):
        obstacles = []
        while len(obstacles) < count:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if [x, y] != self.restaurant and [x, y] not in self.agents and [x, y] not in obstacles:
                obstacles.append([x, y])
        return obstacles

    def maybe_spawn_customer(self):
        if random.random() < CUSTOMER_SPAWN_CHANCE:
            while True:
                x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
                if [x, y] not in self.customers and [x, y] != self.restaurant and [x, y] not in self.obstacles:
                    self.customers.append([x, y])
                    break

    def print_grid(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(self.grid_size):
            row = ""
            for j in range(self.grid_size):
                cell = [i, j]
                if cell in self.agents:
                    row += " A "
                elif cell == self.restaurant:
                    row += " R "
                elif cell in self.customers:
                    row += " C "
                elif cell in self.obstacles:
                    row += " # "
                else:
                    row += " . "
            print(row)
        print(f"\nTime: {self.time_step} | Steps: {self.steps_taken} | Deliveries: {self.completed_deliveries} | Energy: {self.energy}/{MAX_ENERGY}")

    def assign_customer(self, agent_index):
        if not self.customers:
            return None
        ax, ay = self.agents[agent_index]
        assigned = [c for i, c in enumerate(self.agent_targets) if i != agent_index]
        unassigned = [c for c in self.customers if c not in assigned]
        if not unassigned:
            return None
        return min(unassigned, key=lambda c: abs(ax - c[0]) + abs(ay - c[1]))

    def move_agent_toward(self, index, target):
        ax, ay = self.agents[index]
        tx, ty = target
        new_pos = [ax, ay]

        # Try axis-aligned movement while avoiding obstacles and other agents
        if ax < tx and [ax + 1, ay] not in self.obstacles and [ax + 1, ay] not in self.agents:
            new_pos[0] += 1
        elif ax > tx and [ax - 1, ay] not in self.obstacles and [ax - 1, ay] not in self.agents:
            new_pos[0] -= 1
        elif ay < ty and [ax, ay + 1] not in self.obstacles and [ax, ay + 1] not in self.agents:
            new_pos[1] += 1
        elif ay > ty and [ax, ay - 1] not in self.obstacles and [ax, ay - 1] not in self.agents:
            new_pos[1] -= 1

        self.agents[index] = new_pos

    def step(self):
        self.time_step += 1
        self.maybe_spawn_customer()

        for i in range(NUM_AGENTS):
            pos = self.agents[i]
            target = self.agent_targets[i]

            # Recharge if needed
            if self.energy <= 0 and pos != self.restaurant:
                self.move_agent_toward(i, self.restaurant)
                self.steps_taken += 1
                continue
            elif pos == self.restaurant:
                self.energy = MAX_ENERGY

            if target is None or target not in self.customers:
                target = self.assign_customer(i)
                self.agent_targets[i] = target

            if target:
                if pos == target:
                    self.customers.remove(target)
                    self.agent_targets[i] = None
                    self.completed_deliveries += 1
                    print(f"✅ Agent {i} delivered to customer at {target}!")
                    time.sleep(0.4)
                else:
                    self.move_agent_toward(i, target)
                    self.steps_taken += 1
                    self.energy -= 1

        return True


if __name__ == "__main__":
    sim = DeliverySim()
    while True:
        sim.print_grid()
        if not sim.step():
            break
        time.sleep(0.3)
