import os

import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.colors import ListedColormap
from main import RPS, YELLOW, ORANGE, BLUE
import imageio

# SIZE_X = 30
# SIZE_Y = SIZE_X
ITERATIONS = 100


def init_map(color_maps, our_plots, _):
    """
    Helper function to plot data with associated colormap.
    """
    # np.random.seed(19681876)
    pop_size = (SIZE_X, SIZE_Y)
    data = np.random.randint(3, size=pop_size)
    plot_map(color_maps, data, our_plots, _)
    return data


def plot_map(color_maps, data, curr_plots, index):
    fig, axs = plt.subplots(1, 1, figsize=(5, 3),
                            constrained_layout=True, squeeze=False)
    for [ax, c_map] in zip(axs.flat, color_maps):
        ax.pcolormesh(data, cmap=c_map, rasterized=True, vmin=0, vmax=2)

    plt.axis('off')
    plt.title('Lizards Territory')
    plt.savefig(f'./simulation/pic{index}.png')
    curr_plots[index] = f'./simulation/pic{index}.png'
    plt.show()


def generation(current_map):
    for i in range(SIZE_X):
        for j in range(SIZE_Y):
            rand_x = random.choice([-1, 0, 1])
            rand_y = random.choice([-1, 0, 1])
            if limit_check(i, j, rand_x, rand_y):
                other = current_map[i + rand_x][j + rand_y]
            else:
                other = current_map[i][j]
            # if current_map[i][j] == YELLOW and other == YELLOW:
            #     current_map[i][j] = random.choice([BLUE, ORANGE])
            # else:
            #     current_map[i][j] = RPS(current_map[i][j], other)
            current_map[i][j] = RPS(current_map[i][j], other)


def limit_check(i, j, rand_x, rand_y):
    return 0 <= i + rand_x < SIZE_X and 0 <= j + rand_y < SIZE_Y


def count_percentage(oranges_num, blues_num, yellows_num, index):
    o = np.count_nonzero(curr_map == 0)
    b = np.count_nonzero(curr_map == 1)
    y = np.count_nonzero(curr_map == 2)
    tot_pop = o + b + y
    oranges_num[index], blues_num[index], yellows_num[index] = o / tot_pop, b / tot_pop, y / tot_pop
    if o / tot_pop == 1 or b / tot_pop == 1 or y / tot_pop == 1:
        return True


def plot_graph(oranges_num, blues_num, yellows_num):
    plt.title('Simulation Graph')
    plt.xlabel("Generation", fontsize=16)
    plt.ylabel("Morph frequency", fontsize=16)
    plt.plot(np.arange(ITERATIONS), oranges_num, color="orange")
    plt.plot(np.arange(ITERATIONS), blues_num, color="b")
    plt.plot(np.arange(ITERATIONS), yellows_num, color="yellow")
    plt.savefig(f'./simulation/graph.png')
    plt.show()


if __name__ == "__main__":
    global SIZE_Y, SIZE_X
    # sizes = [2, 5, 10, 15, 20, 30]
    sizes = [20]
    iterations = np.zeros(len(sizes))
    for i, size in enumerate(sizes):
        SIZE_X = size
        SIZE_Y = size
        plots = np.array([f'./simulation/pic{ITERATIONS}.png' for _ in range(ITERATIONS)])
        oranges = np.zeros(ITERATIONS)
        blues = np.zeros(ITERATIONS)
        yellows = np.zeros(ITERATIONS)
        color_map = ListedColormap(["darkorange", "blue", "yellow"])
        curr_map = init_map([color_map], plots, 0)
        count_percentage(oranges, blues, yellows, 0)
        for iteration in range(1, ITERATIONS):
            generation(curr_map)
            plot_map([color_map], curr_map, plots, iteration)
            if count_percentage(oranges, blues, yellows, iteration):
                iterations[i] = iteration
                plots = plots[:iteration]
                break
        plot_graph(oranges, blues, yellows)
        with imageio.get_writer('./simulation/sim.gif', mode='I') as writer:
            for filename in plots:
                image = imageio.imread(filename)
                writer.append_data(image)
        for filename in set(plots):
            os.remove(filename)
    plt.title('Extinction')
    plt.xlabel("Population Size", fontsize=16)
    plt.ylabel("time until extinction", fontsize=16)
    plt.plot(sizes, iterations)
    plt.savefig(f'./simulation/extinction.png')
    plt.show()
