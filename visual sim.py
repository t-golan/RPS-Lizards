import os

import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.colors import ListedColormap
from main import RPS
import imageio

SIZE_X = 30
SIZE_Y = SIZE_X
ITERATIONS = 10


# data = np.random.rand(10, 10) * 20

# create discrete colormap
# cmap = colors.ListedColormap(['orange', 'blue'])
# bounds = [0, 10, 20]
# norm = colors.BoundaryNorm(bounds, cmap.N)
#
# fig, ax = plt.subplots()
# ax.imshow(data, cmap=cmap, norm=norm)
#
# draw gridlines
# ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
# ax.set_xticks(np.arange(0, 10, 1))
# ax.set_yticks(np.arange(10, -1, -1))

# plt.show()


def init_map(colormaps, plots, _):
    """
    Helper function to plot data with associated colormap.
    """
    np.random.seed(19681876)
    data = np.random.randn(SIZE_X, SIZE_Y)
    plot_map(colormaps, data, plots, _)
    return data


def plot_map(colormaps, data, plots, index):
    fig, axs = plt.subplots(1, 1, figsize=(5, 3),
                            constrained_layout=True, squeeze=False)
    for [ax, cmap] in zip(axs.flat, colormaps):
        psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=-4, vmax=4)
        # fig.colorbar(psm, ax=ax)

    plt.axis('off')
    plt.title('Lizards Territory')
    plt.savefig(f'./simulation/pic{index}.png')
    plots[index] = f'./simulation/pic{index}.png'
    plt.show()
    return plt


def battle(param, param1):
    return RPS(int(param), int(param1))


def generation(curr_map):
    for i in range(SIZE_X):
        for j in range(SIZE_Y):
            rand_x = random.choice([-1, 0, 1])
            rand_y = random.choice([-1, 0, 1])
            if limit_check(i, j, rand_x, rand_y):
                other = curr_map[i + rand_x][j + rand_y]
            else:
                other = curr_map[i][j]
            curr_map[i][j] = battle(curr_map[i][j], other)


def limit_check(i, j, rand_x, rand_y):
    return 0 <= i + rand_x < SIZE_X and 0 <= j + rand_y < SIZE_Y


if __name__ == "__main__":
    plots = np.array([f'./simulation/pic{ITERATIONS}.png' for _ in range(ITERATIONS)])
    color_map = ListedColormap(["yellow", "darkorange", "blue"])
    curr_map = init_map([color_map], plots, 0)
    for _ in range(1, ITERATIONS):
        generation(curr_map)
        curr_plot = plot_map([color_map], curr_map, plots, _)
    with imageio.get_writer('./simulation/sim.gif', mode='I') as writer:
        for filename in plots:
            image = imageio.imread(filename)
            writer.append_data(image)
    for filename in set(plots):
        os.remove(filename)
