# בתור פמיניסט אני אומר את זה
import random
import numpy as np
import matplotlib.pyplot as plt

ITERATIONS = 100
TOT_AREA = 1000  # includes food?
TOT_FEMALES = 100
INIT_ORANGE_NUM = 1000
INIT_BLUE_NUM = 1000
INIT_YELLOW_NUM = 1000
POP_SIZE = INIT_ORANGE_NUM + INIT_BLUE_NUM + INIT_YELLOW_NUM
FEMALE_FACTOR = 3  # todo: how to determine?
AREA_FACTOR = 3  # todo: how to determine?

ORANGE = 1
BLUE = 2
YELLOW = 3


class World:
    def __init__(self, orange, blue, yellow):
        self.orange = Lizards(ORANGE, orange)
        self.blue = Lizards(BLUE, blue)
        self.yellow = Lizards(YELLOW, yellow)
        self.size = orange + blue + yellow

    def update_size(self):
        self.size = self.orange.amount + self.blue.amount + self.yellow.amount

    def get_amount(self, color):
        if color == ORANGE:
            return self.orange.amount
        if color == BLUE:
            return self.blue.amount
        if color == YELLOW:
            return self.yellow.amount

    def decrease(self, color):
        if color == ORANGE:
            self.orange.amount -= 1
        if color == BLUE:
            self.blue.amount -= 1
        if color == YELLOW:
            self.yellow.amount -= 1


class Lizards:
    def __init__(self, color, amount=0):
        self.amount = amount
        self.color = color
        self.females = self.calc_females()
        self.area = self.calc_area()

    def calc_females(self):
        if self.color == YELLOW:
            return 0
        elif self.color == BLUE:
            return self.amount
        return self.amount * FEMALE_FACTOR

    def calc_area(self):
        if self.color == YELLOW:
            return 0
        elif self.color == BLUE:
            return self.amount
        return self.amount * AREA_FACTOR


def RPS(first, second):
    if first == second:
        return first
    if first == ORANGE or second == ORANGE:
        if first == BLUE or second == BLUE:
            return ORANGE
        return YELLOW
    return BLUE


def get_competitor(pop: World):
    # while True:
    #     competitor = random.randint(1, 3)
    #     if pop.get_amount(competitor) > 0:
    #         pop.decrease(competitor)
    #         return competitor
    pop.update_size()
    competitor = random.randint(1, pop.size)
    for i in range(1, 4):
        if pop.get_amount(i) >= competitor:
            pop.decrease(i)
            return i
        competitor -= pop.get_amount(i)


def calc_yellows(oranges, yellows):
    return min(yellows * 2, oranges * 2)


def equal_next_gen(new_world):
    """
    calculates the production of the next generation -
    everyone doubles itself
    :param new_world:
    :return:
    """
    new_world[ORANGE - 1] *= 2
    new_world[BLUE - 1] *= 2
    new_world[YELLOW - 1] *= 2


def dependant_next_gen(new_world):
    """
    calculates the production of the next generation -
    blue doubles itself
    yellows doubles oranges
    orange fills the rest
    :param new_world:
    :return:
    """
    new_world[ORANGE - 1] = (int(new_world[2] > 0)) * calc_yellows(
        new_world[0], new_world[2])
    new_world[BLUE - 1] *= 2
    new_world[YELLOW - 1] = (int(new_world[0] > 0)) * (
            POP_SIZE - new_world[1] - new_world[2])


def basic_scenario(pop: World):
    """
    randomly chooses pairs from the population and the winner stays to the next generation
    assumptions: area is unlimited, winner blue produces 2 blues, winner yellow produces yellows as a function of the
    oranges, and the oranges produces the rest
    :return:
    """
    new_world = np.zeros(3)
    for i in range(int(pop.size) // 2):
        competitor1 = get_competitor(pop)
        competitor2 = get_competitor(pop)
        winner = RPS(competitor1, competitor2)
        new_world[winner - 1] += 1
    equal_next_gen(new_world)
    return World(new_world[0], new_world[1], new_world[2])


if __name__ == '__main__':
    world = World(INIT_ORANGE_NUM, INIT_BLUE_NUM, INIT_YELLOW_NUM)
    oranges = np.zeros(ITERATIONS)
    blues = np.zeros(ITERATIONS)
    yellows = np.zeros(ITERATIONS)
    for i in range(ITERATIONS):
        oranges[i], blues[i], yellows[i] = \
            world.orange.amount, world.blue.amount, world.yellow.amount
        world = basic_scenario(world)
        # print(oranges[i], blues[i], yellows[i])
    plt.plot(np.arange(ITERATIONS), oranges, color="orange")
    plt.plot(np.arange(ITERATIONS), blues, color="b")
    plt.plot(np.arange(ITERATIONS), yellows, color="yellow")

    # plt.legend(["orange", "blue", "yellow"])
    plt.show()