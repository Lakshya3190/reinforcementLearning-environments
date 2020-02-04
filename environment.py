import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mesa import Agent, Model
from mesa.time import RandomActivation
import time
from math import hypot
from mesa.space import ContinuousSpace

"""
Simple multi-agent model environment using matplotlib 
"""

frUnit_init_locx = 200
frUnit_init_locy = 25

fs_init_locx = 200
fs_init_locy = 14

enemy1_locx = 360
enemy2_locx = 87
enemy3_locx = 37

enemy1_locy = 61
enemy2_locy = 118
enemy3_locy = 320

friendly_unit_health = 2000

path = [(50, 100), (150, 200), (300, 350)]


# Class of Enemy Infantry
class EnInfantry(Agent):
    def __init__(self, unique_id, model, health, loc_x, loc_y, ax):
        super().__init__(unique_id, model)
        self.health = health
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.ax = ax

    def step(self):
        self.ax.plot(self.loc_x, self.loc_y, 'ro', markersize=10)


# Class of Enemy Artillery
class EnArty(Agent):
    def __init__(self, unique_id, model, health, loc_x, loc_y, ax):
        super().__init__(unique_id, model)
        self.health = health
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.ax = ax

    def step(self):
        self.ax.plot(self.loc_x, self.loc_y, 'rs', markersize=20)


# Class of enemy armour
class EnArmour(Agent):
    def __init__(self, unique_id, model, health, loc_x, loc_y, ax):
        super().__init__(unique_id, model)
        self.health = health
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.ax = ax

    def step(self):
        self.ax.plot(self.loc_x, self.loc_y, 'rs', markersize=10)


# Class of friendly unit
class FrUnit(Agent):
    def __init__(self, unique_id, model, health, loc_x, loc_y, ax, ax2):
        super().__init__(unique_id, model)
        self.health = health
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.ax = ax
        self.ax2 = ax2


    def step(self):

        # Movement of Friendly unit
        if self.loc_y < 350:
            self.loc_y = self.loc_y + 1
            self.ax.plot(self.loc_x, self.loc_y, 'go', markersize=10)

            # Determining the distance between each enemy and friendly unit as the unit moves
            dist_enemy1 = hypot(enemy1_locx - self.loc_x, enemy1_locy - self.loc_y)
            dist_enemy2 = hypot(enemy2_locx - self.loc_x, enemy2_locy - self.loc_y)
            dist_enemy3 = hypot(enemy3_locx - self.loc_x, enemy3_locy - self.loc_y)

            if 0 < dist_enemy1 < 200:
                self.ax.plot([self.loc_x, enemy1_locx], [self.loc_y, enemy1_locy], 'r-', linewidth=1)
                self.health = self.health - 2
            elif 200 < dist_enemy1 < 300:
                self.ax.plot([self.loc_x, enemy1_locx], [self.loc_y, enemy1_locy], 'b-', linewidth=1)
                self.health = self.health - 1
            elif 300 < dist_enemy1 < 400:
                self.ax.plot([self.loc_x, enemy1_locx], [self.loc_y, enemy1_locy], 'g-', linewidth=1)
                self.health = self.health - 0.5

            if 0 < dist_enemy2 < 200:
                self.ax.plot([self.loc_x, enemy2_locx], [self.loc_y, enemy2_locy], 'r-', linewidth=1)
                self.health = self.health - 2
            elif 200 < dist_enemy2 < 300:
                self.ax.plot([self.loc_x, enemy2_locx], [self.loc_y, enemy2_locy], 'b-', linewidth=1)
                self.health = self.health - 1
            elif 300 < dist_enemy2 < 400:
                self.ax.plot([self.loc_x, enemy2_locx], [self.loc_y, enemy2_locy], 'g-', linewidth=1)
                self.health = self.health - 0.5

            if 0 < dist_enemy3 < 200:
                self.ax.plot([self.loc_x, enemy3_locx], [self.loc_y, enemy3_locy], 'r-', linewidth=1)
                self.health = self.health - 2
            elif 200 < dist_enemy3 < 300:
                self.ax.plot([self.loc_x, enemy3_locx], [self.loc_y, enemy3_locy], 'b-', linewidth=1)
                self.health = self.health - 1
            elif 300 < dist_enemy3 < 400:
                self.ax.plot([self.loc_x, enemy3_locx], [self.loc_y, enemy3_locy], 'g-', linewidth=1)
                self.health = self.health - 0.5

            self.ax2.plot([self.health], [self.health], 'ro', markersize=3)

# Class of friendly artillery base
class FrArty(Agent):
    def __init__(self, unique_id, model, health, loc_x, loc_y, ax):
        super().__init__(unique_id, model)
        self.health = health
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.ax = ax

    def step(self):
        self.ax.plot(self.loc_x, self.loc_y, 'gs', markersize=30)


# Fire support model
class FireSupportModel(Model):
    def __init__(self, ax, ax2):
        self.schedule = RandomActivation(self)
        self.grid = ContinuousSpace(400, 400, True)
        self.ax = ax
        self.ax2 = ax2

        # Creating all agents
        enemy_inf1 = EnInfantry(1, self, 10, enemy1_locx, enemy1_locy, self.ax)
        self.schedule.add(enemy_inf1)
        self.grid.place_agent(enemy_inf1, (enemy1_locx, enemy1_locy))

        enemy_arty1 = EnArty(10, self, 30, enemy2_locx, enemy2_locy, self.ax)
        self.schedule.add(enemy_arty1)
        self.grid.place_agent(enemy_arty1, (enemy2_locx, enemy2_locy))

        enemy_tank1 = EnArmour(20, self, 20, enemy3_locx, enemy3_locy, self.ax)
        self.schedule.add(enemy_tank1)
        self.grid.place_agent(enemy_tank1, (enemy3_locx, enemy3_locy))

        friendly_unit1 = FrUnit(30, self, friendly_unit_health, frUnit_init_locx, frUnit_init_locy, self.ax, self.ax2)
        self.schedule.add(friendly_unit1)
        self.grid.place_agent(friendly_unit1, (frUnit_init_locx, frUnit_init_locy))

        friendly_arty = FrArty(40, self, 10, fs_init_locx, fs_init_locy, self.ax)
        self.schedule.add(friendly_arty)
        self.grid.place_agent(friendly_arty, (fs_init_locx, fs_init_locy))

    def step(self):
        self.schedule.step()


fig = plt.figure()
ax = fig.add_subplot(1, 2, 2)
plt.grid(b=True, which='major', color='#666666', linestyle='-')
ax2 = fig.add_subplot(2, 2, 1)
fig.suptitle('Fire Support Environment')
plt.grid(b=True, which='major', color='#666666', linestyle='-')

model = FireSupportModel(ax, ax2)


def update(i):
    ax.clear()
    model.step()
    ax.axis([0, 400, 0, 400])
    ax2.axis([0, 2000, 0, 2000])
    plt.grid(b=True, which='major', color='#666666', linestyle='-')


ax.clear()

ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 10, 0.1), interval=10)
plt.show()
