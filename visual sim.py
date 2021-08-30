import os

import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.colors import ListedColormap
from main import RPS, create_graph
import imageio

SIZE_X = 30
SIZE_Y = SIZE_X
ITERATIONS = 1000


def init_map(colormaps, plots, _):
    """
    Helper function to plot data with associated colormap.
    """
    # np.random.seed(19681876)
    pop_size = (SIZE_X, SIZE_Y)
    data = np.random.randint(3, size=pop_size)
    plot_map(colormaps, data, plots, _)
    return data


def plot_map(colormaps, data, plots, index):
    fig, axs = plt.subplots(1, 1, figsize=(5, 3),
                            constrained_layout=True, squeeze=False)
    for [ax, cmap] in zip(axs.flat, colormaps):
        psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=0, vmax=2)
        # fig.colorbar(psm, ax=ax)

    plt.axis('off')
    plt.title('Lizards Territory')
    plt.savefig(f'./simulation/pic{index}.png')
    plots[index] = f'./simulation/pic{index}.png'
    # plt.show()
    return plt


def generation(current_map):
    for i in range(SIZE_X):
        for j in range(SIZE_Y):
            rand_x = random.choice([-1, 0, 1])
            rand_y = random.choice([-1, 0, 1])
            if limit_check(i, j, rand_x, rand_y):
                other = current_map[i + rand_x][j + rand_y]
            else:
                other = current_map[i][j]
            current_map[i][j] = RPS(current_map[i][j], other)


def limit_check(i, j, rand_x, rand_y):
    return 0 <= i + rand_x < SIZE_X and 0 <= j + rand_y < SIZE_Y


def count_percentage(oranges_num, blues_num, yellows_num, index):
    o = np.count_nonzero(curr_map == 0)
    b = np.count_nonzero(curr_map == 1)
    y = np.count_nonzero(curr_map == 2)
    tot_pop = o + b + y
    oranges_num[index], blues_num[index], yellows_num[index] = o / tot_pop, b / tot_pop, y / tot_pop


def plot_graph(oranges_num, blues_num, yellows_num):
    plot = create_graph(oranges_num, blues_num, yellows_num, ITERATIONS)
    plot.savefig(f'./simulation/graph.png')
    plot.show()


if __name__ == "__main__":
    plots = np.array([f'./simulation/pic{ITERATIONS}.png' for _ in range(ITERATIONS)])
    oranges = np.zeros(ITERATIONS)
    blues = np.zeros(ITERATIONS)
    yellows = np.zeros(ITERATIONS)
    color_map = ListedColormap(["yellow", "darkorange", "blue"])
    curr_map = init_map([color_map], plots, 0)
    count_percentage(oranges, blues, yellows, 0)
    for _ in range(1, ITERATIONS):
        generation(curr_map)
        curr_plot = plot_map([color_map], curr_map, plots, _)
        count_percentage(oranges, blues, yellows, _)
    plot_graph(oranges, blues, yellows)
    with imageio.get_writer('./simulation/sim.gif', mode='I') as writer:
        for filename in plots:
            image = imageio.imread(filename)
            writer.append_data(image)
    for filename in set(plots):
        os.remove(filename)
