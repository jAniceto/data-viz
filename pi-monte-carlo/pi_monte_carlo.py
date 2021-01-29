import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.rcParams.update({
    "text.usetex": True,
})


def run_simulation(runs=1000):
    simulation = []
    circle_points = 0
    for i in range(runs):
        # Create a (x, y) point at random
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        
        # Check if the point falls within the circle
        if x**2 + y**2 <= 1:
            circle_points += 1

        # Calculate current pi value
        pi_estimate = 4 * circle_points/(i+1)

        # Save simulation step
        simulation.append([x, y, pi_estimate])

    # Print final pi value
    print('Result: Pi =', simulation[-1][2])
    return simulation


def visualize(simulation):
    plt.figure()
    ax = plt.axes(xlim=(-1, 1), ylim=(-1, 1))
    ax.set_aspect('equal', 'box')
    
    for it in simulation:
        x, y, estimate = it
        if x**2 + y**2 <= 1:
            color = '#c0392b'  # red
        else:
            color = '#2980b9'  # blue
        plt.plot(x, y, marker='o', color=color, markersize=2)
    
    plt.title(f"$n = {len(simulation)}, \pi \\approx {simulation[-1][2]:.6f}$")


def animation(simulation):
    fig = plt.figure()
    ax = plt.axes(xlim=(-1, 1), ylim=(-1, 1))
    ax.set_aspect('equal', 'box')
    scat = plt.scatter(x=[], y=[], marker='o')

    def animation_update(i):
        xx = [x[0] for x in simulation[:i]]
        yy = [y[1] for y in simulation[:i]]
        colors = []
        for it in simulation[:i]:
            x, y, estimate = it
            if x**2 + y**2 <= 1:
                colors.append('r')
            else:
                colors.append('b')
        scat.set_offsets(np.c_[xx, yy])
        scat.set_color(colors[:i])
        scat.set_facecolor(colors[:i])
        return scat,

    anim = FuncAnimation(fig, animation_update, frames=len(simulation), interval=25, blit=True, repeat=False)
    anim.save('figures/animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])


def estimation_evolution(simulation):
    estimations = [x[2] for x in simulation]
    plt.figure()
    plt.plot([0, len(estimations)], [math.pi, math.pi], '--k')
    plt.plot(estimations, '-')
    plt.xlabel('Run')
    plt.ylabel('$\pi$ estimation')
    plt.title(f"$n = {len(simulation)}, \pi \\approx {simulation[-1][2]:.6f}$")


def save_multiple_simulations():
    RUNS = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
    for n in RUNS:
        sim = run_simulation(runs=n)
        visualize(sim)
        plt.savefig(f'figures/sim{n}.png')


if __name__ == '__main__':
    sim = run_simulation(runs=1000000)
    visualize(sim)
    # animation(sim)
    # estimation_evolution(sim)
    plt.show()

    # save_multiple_simulations()