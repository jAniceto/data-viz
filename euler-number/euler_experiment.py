import random
import math
from matplotlib import pyplot as plt


# Configuration
plt.style.use('science')
N = 100_000  # Number of runs per simulation
S = 15  # Number of simulations to run


def pick_numbers_until_sum_one():
    """Pick real numbers at random until their sum is greater than 1.
    Returns the number of number that were picked.
    """
    sum_ = 0
    number_count = 0
    while sum_ < 1:
        number = random.uniform(0, 1)
        sum_ += number
        number_count += 1
    return number_count


def simulate(runs):
    numbers_needed = []
    averages = []
    deviations = []
    for i in range(runs):
        numbers_needed.append(pick_numbers_until_sum_one())
        avg = sum(numbers_needed) / len(numbers_needed)
        averages.append(avg)
        dev = (avg - math.e) / math.e * 100
        deviations.append(dev)

    print(f"Average is {averages[-1]}")
    print(f"Deviation is {deviations[-1]} %")

    iterations = list(range(1,N+1))

    if S == 1:
        # Estimation over runs (overall)
        fig, ax1 = plt.subplots()
        ax1.plot(iterations, averages, '-')
        ax1.plot([iterations[0], iterations[-1]], [math.e, math.e], '-')
        ax1.set_xlabel('Simulation number')
        ax1.set_ylabel('Average')
        ax1.legend([
            f"Estimation ($e$ = {averages[-1]})", 
            "Euler's number ($e$ = 2.71828)"
        ])
        fig.savefig('euler-sim.png', dpi=300, bbox_inches='tight')

        # Estimation over runs (initial iterations)
        fig2, ax2 = plt.subplots()
        ax2.plot(iterations, averages, '-')
        ax2.plot([iterations[0], iterations[-1]], [math.e, math.e], '-')
        ax2.set_xlabel('Simulation number')
        ax2.set_ylabel('Average')
        ax2.legend([
            f"Estimation ($e$ = {averages[-1]})", 
            "Euler's number ($e$ = 2.71828)"
        ])
        ax2.set_xlim(-250, 5000)
        fig2.savefig('euler-sim-begin.png', dpi=300, bbox_inches='tight')

        # Estimation over runs (overall but in log scale for x)
        fig3, ax3 = plt.subplots()
        ax3.semilogx(iterations, averages, '-')
        ax3.semilogx([iterations[0], iterations[-1]], [math.e, math.e], '-')
        ax3.set_xlabel('Simulation number')
        ax3.set_ylabel('Average')
        ax3.legend([
            f"Estimation ($e$ = {averages[-1]})", 
            "Euler's number ($e$ = 2.71828)"
        ])
        ax3.set_xlim(1, runs)
        fig3.savefig('euler-sim-log.png', dpi=300, bbox_inches='tight')

    # Plot e estimation over the iterations in log scale
    ax_log.semilogx(iterations, averages, '-', color='#0C5DA5', alpha=0.8)
    ax_log.semilogx([iterations[0], iterations[-1]], [math.e, math.e], '-', color='#00B438')

    return averages[-1]
    

if __name__ == '__main__':
    fig_log, ax_log = plt.subplots()
    
    for _ in range(S):
        simulate(N)

    ax_log.set_xlabel('$\log$ Simulation number')
    ax_log.set_ylabel('Average')
    ax_log.set_xlim(1, N)
    fig_log.savefig('euler-many-sim-log.png', dpi=300, bbox_inches='tight')

    plt.show()