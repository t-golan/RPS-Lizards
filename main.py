import random
import numpy as np
import matplotlib.pyplot as plt

ITERATIONS = 100
TOT_AREA = 1000  # includes food?
TOT_FEMALES = 100
INIT_ORANGE_NUM = 100
INIT_BLUE_NUM = 100
INIT_YELLOW_NUM = 100
POP_SIZE = INIT_ORANGE_NUM + INIT_BLUE_NUM + INIT_YELLOW_NUM
MUTATION_RATE = 0.1

ORANGE = 0
BLUE = 1
YELLOW = 2


class World:
    def __init__(self, orange, blue, yellow):
        """
        initiates a population of Trimorphic lizards
        :param orange:
        :param blue:
        :param yellow:
        """
        self.orange = orange
        self.blue = blue
        self.yellow = yellow
        self.size = orange + blue + yellow

    def update_size(self):
        """
        updates the size of the population
        """
        self.size = self.orange + self.blue + self.yellow

    def get_amount(self, color):
        """
        returns the amount of lizards of requested color
        :param color: the color of the lizards we want
        :return: an int
        """
        if color == ORANGE:
            return self.orange
        if color == BLUE:
            return self.blue
        if color == YELLOW:
            return self.yellow

    def decrease(self, color):
        """
        removes a lizards from the population after it was chosen
        :param color: the color of chosen lizard
        """
        if color == ORANGE:
            self.orange -= 1
        if color == BLUE:
            self.blue -= 1
        if color == YELLOW:
            self.yellow -= 1


def RPS(first, second):
    """
    basic rules of the game - orange beats blue, blue beats yellow and yellow beats orange
    :param first: int represents the color of the first lizard
    :param second: int represents the color of the second lizard
    :return: the color of the winner
    """
    if first == second:
        return first
    if first == ORANGE or second == ORANGE:
        if first == BLUE or second == BLUE:
            return ORANGE
        return YELLOW
    return BLUE


def get_competitor(pop: World):
    """
    randomly chooses one lizard from the population
    :param pop: the current population
    :return: one chosen color of lizard which is still available in the population
    """
    competitor = random.randint(1, pop.size)
    for i in range(0, 3):
        if pop.get_amount(i) >= competitor:
            pop.decrease(i)
            pop.update_size()
            return i
        competitor -= pop.get_amount(i)


def return_competitor(pop: World, competitor):
    """
    returns a competitor to the population
    :param pop: the current population
    :param competitor: the color of the competitor to be returned
    """
    if competitor == YELLOW:
        pop.yellow += 1
    elif competitor == ORANGE:
        pop.orange += 1
    elif competitor == BLUE:
        pop.blue += 1
    pop.update_size()


def calc_depended(predator, pred):
    """

    :param pred:
    :param predator:
    :return:
    """
    return int(min(predator * 2.3, pred * 2.3))


def mutate():
    chance = random.uniform(0, 1)
    if chance < MUTATION_RATE:
        return True
    return False


def equal_next_gen(new_world):
    """
    calculates the production of the next generation -
    everyone doubles itself
    :param new_world: the distribution of the next generation
    """
    new_world[ORANGE] = int(new_world[ORANGE] * 2)
    new_world[BLUE] = int(new_world[BLUE] * 2)  # also changed here?
    new_world[YELLOW] = int(new_world[YELLOW] * 2)
    for _ in range(POP_SIZE):
        if mutate():
            new_world[random.randrange(0, 3)] += 1
            new_world[random.randrange(0, 3)] -= 1
    # extinct = no_extinct(new_world)
    # if extinct:
          # new_world[new_world.argmax()] //= 1.035
          # print("extincted", new_world[ORANGE], new_world[BLUE], new_world[YELLOW])


def equal_distributed_next_gen(new_world, num):
    """
    calculates the production of the next generation -
    everyone doubles itself
    :param new_world: the distribution of the next generation
    """
    div = 2
    new_world[ORANGE] = round(new_world[ORANGE] * div)
    new_world[BLUE] = round(new_world[BLUE] * div)
    new_world[YELLOW] = round(new_world[YELLOW] * div)
    for i in range(num, 2 * num):
        new_world[i % 3] += 1


def no_extinct(new_world):
    """
    prevents an occasion of extinction of one of the morphs
    :param new_world: the distribution of the next generation
    """
    if new_world[BLUE] < 1:
        new_world[BLUE] = 1
    if new_world[YELLOW] < 1:
        new_world[YELLOW] = 1
    if new_world[ORANGE] < 1:
        new_world[ORANGE] = 1


def dependant_next_gen(new_world):
    """
    calculates the production of the next generation -
    blue ___ itself
    yellows ___ oranges
    orange ___ the rest
    :param new_world: the distribution of the next generation
    """
    new_world[YELLOW] = calc_depended(new_world[ORANGE], new_world[YELLOW])
    new_world[BLUE] = calc_depended(new_world[BLUE], new_world[ORANGE])
    new_world[ORANGE] = int((POP_SIZE - new_world[BLUE] - new_world[YELLOW]))
    # new_world[ORANGE] = int(1.7 * new_world[BLUE])
    # no_extinct(new_world)


def basic_scenario(pop: World):
    """
    randomly chooses pairs from the population and the winner stays to the next generation
    assumptions: area is unlimited, winner blue produces 2 blues, winner yellow produces yellows as a function of the
    oranges, and the oranges produces the rest
    :return: World of the next generation
    """
    new_world = np.zeros(3)
    for _ in range(int(pop.size) // 2):
        competitor1 = get_competitor(pop)
        competitor2 = get_competitor(pop)
        winner = RPS(competitor1, competitor2)
        new_world[winner] += 1
    # dependant_next_gen(new_world)
    equal_next_gen(new_world)
    return World(new_world[ORANGE], new_world[BLUE], new_world[YELLOW])


def diff_basic_scenario(pop: World):
    """
    ???
    :param pop: the current population
    :return: World of the next generation
    """
    new_world = np.zeros(3)
    competitor1 = get_competitor(pop)
    for i in range(int(pop.size) - 1):
        competitor2 = get_competitor(pop)
        winner = RPS(competitor1, competitor2)
        if winner == competitor2:
            competitor1 = competitor2
        new_world[winner] += 1
    dependant_next_gen(new_world)
    return World(new_world[ORANGE], new_world[BLUE], new_world[YELLOW])


def eating_scenario(pop: World):
    """
    model where one color has to beat different color in order to survive to thee next generation
    :param pop: the current population
    :return: World of the next generation
    """
    new_world = np.zeros(3)
    for _ in range(int(pop.size) // 2):
        competitor1, competitor2 = get_competitor(pop), get_competitor(pop)
        while competitor1 == competitor2:  # we don't like ties
            # only one color left
            if (pop.yellow + pop.orange == 0 or
                    pop.yellow + pop.blue == 0 or
                    pop.blue + pop.orange == 0):
                return_competitor(pop, competitor1)
                return_competitor(pop, competitor2)
                equal_distributed_next_gen(new_world, int(pop.yellow + pop.orange + pop.blue))
                return World(new_world[ORANGE], new_world[BLUE], new_world[YELLOW])
            return_competitor(pop, competitor2)
            competitor2 = get_competitor(pop)
        winner = RPS(competitor1, competitor2)
        new_world[winner] += 1
    equal_distributed_next_gen(new_world, 0)
    return World(new_world[ORANGE], new_world[BLUE], new_world[YELLOW])


def live_long_and_prosper(pop: World):
    """
    basically an easter egg
    :param pop: the current population
    :return: World of the next generation
    """
    new_world = np.zeros(3)
    for _ in range(int(pop.size) // 2):
        competitor1 = get_competitor(pop)
        new_world[competitor1] += 1
        competitor2 = get_competitor(pop)
        winner = RPS(competitor1, competitor2)
        new_world[winner] += 1
    return World(new_world[ORANGE], new_world[BLUE], new_world[YELLOW])


def pred_predator_scenario(pop: World, params):
    """

    :param pop: the current population
    :param params: specific parameters which control the generation of the next generation
    :return: World of the next generation
    """
    new_world = np.zeros(3)
    for i in range(3):
        new_world[i] = params[3 * i] * pop.get_amount(i) + params[3 * i + 1] * pop.get_amount(
            (i + 1) % 3) - params[3 * i + 2] * pop.get_amount((i + 2) % 3)
        if new_world[i] < 1:
            new_world[i] = 1
    return World(new_world[ORANGE], new_world[BLUE], new_world[YELLOW])


def create_graph(oranges_num, blues_num, yellows_num, length):
    plt.plot(np.arange(length), oranges_num, color="orange")
    plt.plot(np.arange(length), blues_num, color="b")
    plt.plot(np.arange(length), yellows_num, color="yellow")
    plt.xlabel("Generation", fontsize=16)
    plt.ylabel("Morph frequency", fontsize=16)
    return plt


if __name__ == '__main__':
    world = World(INIT_ORANGE_NUM, INIT_BLUE_NUM, INIT_YELLOW_NUM)
    oranges = np.zeros(ITERATIONS)
    blues = np.zeros(ITERATIONS)
    yellows = np.zeros(ITERATIONS)
    for i in range(ITERATIONS):
        tot_pop = world.orange + world.blue + world.yellow
        oranges[i], blues[i], yellows[i] = world.orange / tot_pop, world.blue / tot_pop, world.yellow / tot_pop
        world = basic_scenario(world)  # trial 2
        # world = live_long_and_prosper(world)  # trial 2
        # world = eating_scenario(world)  # trial 1
        # world = pred_predator_scenario(world, (1.01, 0.55, 0.3, 1.085, 0.55,
        #                                        0.5443256027512, 0.6, 0.4, 0.25))  # trial 4 - stable but blue extincts
    plt = create_graph(oranges, blues, yellows, ITERATIONS)
    plt.show()
