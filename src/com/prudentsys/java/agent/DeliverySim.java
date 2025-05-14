package com.prudentsys.agent;

import java.util.*;

public class DeliverySim {
    static final int GRID_SIZE = 6;
    static final int OBSTACLE_COUNT = 8;
    static final int MAX_ENERGY = 20;
    static final int NUM_AGENTS = 2;
    static final double CUSTOMER_SPAWN_CHANCE = 0.3;

    int[][] grid = new int[GRID_SIZE][GRID_SIZE];
    List<int[]> agents = new ArrayList<>();
    List<int[]> customers = new ArrayList<>();
    List<int[]> obstacles = new ArrayList<>();
    List<int[]> agentTargets = new ArrayList<>();
    int[] restaurant = {0, 0};

    int energy = MAX_ENERGY;
    int steps = 0;
    int deliveries = 0;
    int time = 0;
    Random rand = new Random();

    public DeliverySim() {
        for (int i = 0; i < NUM_AGENTS; i++) {
            agents.add(new int[]{restaurant[0], restaurant[1]});
            agentTargets.add(null);
        }
        spawnObstacles();
    }

    void spawnObstacles() {
        while (obstacles.size() < OBSTACLE_COUNT) {
            int x = rand.nextInt(GRID_SIZE);
            int y = rand.nextInt(GRID_SIZE);
            int[] pos = {x, y};
            if (!isSame(pos, restaurant) && !contains(obstacles, pos) && !contains(agents, pos)) {
                obstacles.add(pos);
            }
        }
    }

    void maybeSpawnCustomer() {
        if (rand.nextDouble() < CUSTOMER_SPAWN_CHANCE) {
            while (true) {
                int x = rand.nextInt(GRID_SIZE);
                int y = rand.nextInt(GRID_SIZE);
                int[] pos = {x, y};
                if (!contains(customers, pos) && !isSame(pos, restaurant) && !contains(obstacles, pos)) {
                    customers.add(pos);
                    break;
                }
            }
        }
    }

    void moveAgentToward(int index, int[] target) {
        int[] pos = agents.get(index);
        int ax = pos[0], ay = pos[1];
        int tx = target[0], ty = target[1];

        int[] newPos = Arrays.copyOf(pos, 2);
        if (ax < tx && !isBlocked(ax + 1, ay)) newPos[0]++;
        else if (ax > tx && !isBlocked(ax - 1, ay)) newPos[0]--;
        else if (ay < ty && !isBlocked(ax, ay + 1)) newPos[1]++;
        else if (ay > ty && !isBlocked(ax, ay - 1)) newPos[1]--;

        agents.set(index, newPos);
        steps++;
        energy--;
    }

    boolean isBlocked(int x, int y) {
        int[] pos = {x, y};
        return x < 0 || x >= GRID_SIZE || y < 0 || y >= GRID_SIZE || contains(obstacles, pos) || contains(agents, pos);
    }

    void printGrid() {
        System.out.print("\033[H\033[2J"); // clear console
        System.out.flush();

        for (int i = 0; i < GRID_SIZE; i++) {
            for (int j = 0; j < GRID_SIZE; j++) {
                int[] pos = {i, j};
                if (contains(agents, pos)) System.out.print(" A ");
                else if (isSame(pos, restaurant)) System.out.print(" R ");
                else if (contains(customers, pos)) System.out.print(" C ");
                else if (contains(obstacles, pos)) System.out.print(" # ");
                else System.out.print(" . ");
            }
            System.out.println();
        }
        System.out.printf("⏱️ Time: %d | 🚶 Steps: %d | ✅ Deliveries: %d | ⚡ Energy: %d/%d\n\n",
                time, steps, deliveries, energy, MAX_ENERGY);
    }

    void assignTargets() {
        for (int i = 0; i < NUM_AGENTS; i++) {
            if (agentTargets.get(i) == null || !contains(customers, agentTargets.get(i))) {
                int[] current = agents.get(i);
                int[] closest = null;
                int minDist = Integer.MAX_VALUE;

                for (int[] c : customers) {
                    if (agentTargets.contains(c)) continue;
                    int dist = Math.abs(current[0] - c[0]) + Math.abs(current[1] - c[1]);
                    if (dist < minDist) {
                        minDist = dist;
                        closest = c;
                    }
                }
                agentTargets.set(i, closest);
            }
        }
    }

    void step() {
        time++;
        maybeSpawnCustomer();
        assignTargets();

        for (int i = 0; i < NUM_AGENTS; i++) {
            int[] pos = agents.get(i);
            int[] target = agentTargets.get(i);

            if (energy <= 0 && !isSame(pos, restaurant)) {
                moveAgentToward(i, restaurant);
                continue;
            } else if (isSame(pos, restaurant)) {
                energy = MAX_ENERGY;
            }

            if (target != null) {
                if (isSame(pos, target)) {
                    customers.removeIf(c -> isSame(c, target));
                    agentTargets.set(i, null);
                    deliveries++;
                    System.out.printf("✅ Agent %d delivered to customer at (%d,%d)\n", i, target[0], target[1]);
                } else {
                    moveAgentToward(i, target);
                }
            }
        }
    }

    boolean contains(List<int[]> list, int[] pos) {
        for (int[] p : list) {
            if (isSame(p, pos)) return true;
        }
        return false;
    }

    boolean isSame(int[] a, int[] b) {
        return a[0] == b[0] && a[1] == b[1];
    }

    public static void main(String[] args) throws InterruptedException {
        DeliverySim sim = new DeliverySim();
        while (true) {
            sim.printGrid();
            sim.step();
            Thread.sleep(300);
        }
    }
}

