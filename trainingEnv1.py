import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mesa import Agent, Model
from mesa.time import BaseScheduler
import time
from math import hypot
from mesa.space import ContinuousSpace

"""
Simple multi-agent model environment using matplotlib 
"""

enemy1_loc = (340, 61)
enemy2_loc = (170, 118)
enemy3_loc = (220, 320)

frUnit_init_loc = (200, 25)
fsUnit_loc = (200, 14)

friendly_unit_health = 2000

path = [(200, 100), (150, 200), (300, 350)]

ammunition_light_round = 100
ammunition_heavy_round = 100


# Class of Enemy Infantry
class EnInfantry(Agent):
    def __init__(self, unique_id, model, health, loc_x, loc_y, ax, target_loc, self_loc):
        super().__init__(unique_id, model)
        self.health = health
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.ax = ax
        self.target_loc = target_loc
        self.self_loc = self_loc
        self.destroyed = False
        self.armour = 0.5

    def health_drain(self, damage_sustained):
        self.health = self.health - damage_sustained
        if self.health == 0:
            self.destroyed = True
            print(self.destroyed)

    def fire(self):
        target = self.model.schedule.agents[1]
        if self.model.grid.get_distance(self.self_loc, self.target_loc) < 100:
            target.health_drain(2)
        if self.destroyed:
            target.health_drain(0)

    def step(self):
        self.fire()
        self.ax.plot(self.loc_x, self.loc_y, 'ro', markersize=4)


# Class of Enemy Artillery
class EnArty(Agent):
    def __init__(self, unique_id, model, health, loc_x, loc_y, ax, target_loc, self_loc):
        super().__init__(unique_id, model)
        self.health = health
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.ax = ax
        self.target_loc = target_loc
        self.self_loc = self_loc
        self.destroyed = False
        self.armour = 2.5

    def health_drain(self, damage_sustained):
        self.health = self.health - damage_sustained
        if self.health == 0:
            self.destroyed = True
            print(self.destroyed)

    def fire(self):
        target = self.model.schedule.agents[1]
        if self.model.grid.get_distance(self.self_loc, self.target_loc) < 100:
            target.health_drain(4)
        if self.destroyed:
            target.health_drain(0)

    def step(self):
        self.fire()
        self.ax.plot(self.loc_x, self.loc_y, 'rs', markersize=6)


# Class of enemy armour
class EnArmour(Agent):
    def __init__(self, unique_id, model, health, loc_x, loc_y, ax, target_loc, self_loc):
        super().__init__(unique_id, model)
        self.health = health
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.ax = ax
        self.target_loc = target_loc
        self.self_loc = self_loc
        self.destroyed = False
        self.armour = 1.8

    def health_drain(self, damage_sustained):
        self.health = self.health - damage_sustained
        if self.health == 0:
            self.destroyed = True
            print(self.destroyed)

    def fire(self):
        target = self.model.schedule.agents[1]
        if self.model.grid.get_distance(self.self_loc, self.target_loc) < 100:
            target.health_drain(3)
        if self.destroyed:
            target.health_drain(0)

    def step(self):
        self.fire()
        # print(self.health)
        # if self.health < 0:

        self.ax.plot(self.loc_x, self.loc_y, 'rs', markersize=4)


# Class of friendly unit
class FrUnit(Agent):
    def __init__(self, unique_id, model, health, loc_x, loc_y, ax, ax2, self_loc):
        super().__init__(unique_id, model)
        self.health = health
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.ax = ax
        self.ax2 = ax2
        self.self_loc = self_loc

    def health_drain(self, damage_sustained):
        self.health = self.health - damage_sustained

        return self.health

    def move(self):
        milestones = []
        for milestone in path:
            self.model.grid.move_agent(self, milestone)
            self.ax.plot(milestone[0], milestone[1], 'go', markersize=5)
            milestones.append(milestone)

        self.ax.plot([self.loc_x, milestones[0][0], milestones[1][0], milestones[2][0]],
                     [self.loc_y, milestones[0][1], milestones[1][1], milestones[2][1], ], 'g--', linewidth=1)

    def find_neighbor_close(self):
        enemy_range_low = self.model.grid.get_neighbors(self.self_loc, 100, include_center=True)
        return enemy_range_low

    def find_neighbor_med(self):
        enemy_range_med = self.model.grid.get_neighbors(self.self_loc, 250, include_center=True)
        return enemy_range_med

    def find_neighbor_far(self):
        enemy_range_high = self.model.grid.get_neighbors(self.self_loc, 450, include_center=True)
        return enemy_range_high

    def step(self):
        self.move()
        print(self.health)
        self.ax2.plot([self.health], [self.health], 'go', markersize=3)


# Class of friendly artillery base
class FrArty(Agent):
    def __init__(self, unique_id, model, health, loc_x, loc_y, ax, target_loc, self_loc, heavy_rounds,
                 light_rounds):
        super().__init__(unique_id, model)
        self.health = health
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.ax = ax
        self.target_loc = target_loc
        self.self_loc = self_loc
        self.heavy_rounds = heavy_rounds
        self.light_rounds = light_rounds

    def health_drain(self, damage):
        pass

    def fire(self):

        # For enemies with high priority
        high_priority_target = self.model.schedule.agents[1].find_neighbor_close()
        for i in high_priority_target:
            if i == FrArty or i == FrUnit:
                high_priority_target.remove(i)
            else:
                break
        # print(high_priority_target)
        if len(high_priority_target) == 0:
            flag = 0
        else:
            flag = 1

        if flag == 1:
            for i in high_priority_target:
                if i != self.model.schedule.agents[1]:
                    i.health_drain(4)
                    self.heavy_rounds = self.heavy_rounds - 2
                else:
                    i.health_drain(0)

        # For enemies with medium priority
        med_priority_target = self.model.schedule.agents[1].find_neighbor_med()
        # print("Med Priority", med_priority_target)
        for i in med_priority_target:
            if i == FrArty or i == FrUnit:
                med_priority_target.remove(i)
            else:
                break
        # med_priority_target.remove(FrUnit)

        if len(med_priority_target) == 0:
            flag1 = 0
        else:
            flag1 = 1

        if flag1 == 1:
            for i in high_priority_target:
                i.health_drain(2)
                self.heavy_rounds = self.heavy_rounds - 1

        # For enemies with low priority
        low_priority_target = self.model.schedule.agents[1].find_neighbor_far()
        for i in low_priority_target:
            if i.unique_id == 11 or i.unique_id == 10:
                low_priority_target.remove(i)
            else:
                break
        print("Low Priority", low_priority_target)
        # low_priority_target.remove(FrUnit)
        if len(med_priority_target) == 0:
            flag2 = 0
        else:
            flag2 = 1

        if flag2 == 1:
            for i in low_priority_target:
                i.health_drain(1)
                self.light_rounds = self.light_rounds - 1
        '''
        print(self.heavy_rounds)
        if self.light_rounds < 0:
            print("Out of Light Ammo")
        if self.heavy_rounds < 0:
            print("Out of heavy ammo")
        '''

    def step(self):
        self.fire()
        # low_priority_target = self.model.schedule.agents[1].find_neighbor_far()
        # print(low_priority_target)
        self.ax.plot(self.loc_x, self.loc_y, 'gs', markersize=8)


# Fire support model
class FireSupportModel(Model):
    def __init__(self, ax, ax2):
        self.schedule = BaseScheduler(self)
        self.grid = ContinuousSpace(400, 400, True)
        self.ax = ax
        self.ax2 = ax2

        # Creating all agents
        # All agents are activated in the order they are added to the scheduler.
        friendly_arty = FrArty(10, self, 10, fsUnit_loc[0], fsUnit_loc[1], self.ax, enemy1_loc, fsUnit_loc,
                               ammunition_heavy_round, ammunition_light_round)
        self.schedule.add(friendly_arty)
        self.grid.place_agent(friendly_arty, (fsUnit_loc[0], fsUnit_loc[1]))

        friendly_unit1 = FrUnit(11, self, friendly_unit_health, frUnit_init_loc[0], frUnit_init_loc[1], self.ax,
                                self.ax2, fsUnit_loc)
        self.schedule.add(friendly_unit1)
        self.grid.place_agent(friendly_unit1, (frUnit_init_loc[0], frUnit_init_loc[1]))

        enemy_inf1 = EnInfantry(1, self, 20, enemy1_loc[0], enemy1_loc[1], self.ax, fsUnit_loc, enemy1_loc)
        self.schedule.add(enemy_inf1)
        self.grid.place_agent(enemy_inf1, (enemy1_loc[0], enemy1_loc[1]))

        enemy_arty1 = EnArty(2, self, 20, enemy2_loc[0], enemy2_loc[1], self.ax, fsUnit_loc, enemy2_loc)
        self.schedule.add(enemy_arty1)
        self.grid.place_agent(enemy_arty1, (enemy2_loc[0], enemy2_loc[1]))

        enemy_tank1 = EnArmour(3, self, 20, enemy3_loc[0], enemy3_loc[1], self.ax, fsUnit_loc, enemy3_loc)
        self.schedule.add(enemy_tank1)
        self.grid.place_agent(enemy_tank1, (enemy3_loc[0], enemy3_loc[1]))

        # print(self.schedule.agents[1])

    def step(self):
        self.schedule.step()
