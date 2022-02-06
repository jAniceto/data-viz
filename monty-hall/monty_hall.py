import random
import matplotlib
from matplotlib import pyplot as plt


# Configuration
# matplotlib.use('TkAgg')
plt.style.use('science')
N = 100_000


def simulate_game(switch=True):
    """ 
    Simulate a single game of the Monty Hall problem. 
    
    If 'switch' is True, the contestant will switch their initially chosen door when offered the chance. 
    
    Returns a True if the contestant won.

    Doors are numbered 0 to 2 (3 doors total).
    """
    DOORS = [0, 1, 2]

    # Prize door
    car_door = random.choices(DOORS)[0]

    # Contestant choses a door
    contestant_door = random.choices(DOORS)[0]

    # Host opens one doors without prize
    host_cant_choose = [car_door, contestant_door]
    host_options = [x for x in DOORS if x not in host_cant_choose]
    host_door = random.choices(host_options)[0]

    # If contestant switches doors
    if switch:
        selected_doors = [contestant_door, host_door]
        contestant_door = [x for x in DOORS if x not in selected_doors][0]

    # Check if contestant won
    if contestant_door == car_door:
        return True
        
    return False


def plot_win_rate(no_switch, switch):
    """Plot win rate over games.
    """
    runs = list(range(1,N+1))

    no_switch_win_rates = []
    no_switch_wins = 0
    for run in runs:
        if no_switch[run-1] == True:
            no_switch_wins += 1  
        no_switch_win_rates.append(no_switch_wins / run * 100)

    switch_win_rates = []
    switch_wins = 0
    for run in runs:
        if switch[run-1] == True:
            switch_wins += 1  
        switch_win_rates.append(switch_wins / run * 100)


    fig1, ax1 = plt.subplots()
    ax1.semilogx(runs, no_switch_win_rates, '-')
    ax1.semilogx(runs, switch_win_rates, '-')
    ax1.set_xlabel('Simulation number')
    ax1.set_ylabel('Win rate (\%)')
    plt.legend(['Never switches', 'Always switches'])
    
    fig1.savefig('monty-hall.png', dpi=300, bbox_inches='tight')


def run_multiple_sims(n_sims):

    runs = list(range(1,N+1))

    fig2, ax2 = plt.subplots()

    for _ in range(n_sims):
        # Run N simulations where the contestant never switches doors
        results_no_switch = []
        for i in range(N):
            results_no_switch.append(simulate_game(switch=False))

        # Run N simulations where the contestant always switches doors
        results_switch = []
        for i in range(N):
            results_switch.append(simulate_game(switch=True))

        no_switch_win_rates = []
        no_switch_wins = 0
        for run in runs:
            if results_no_switch[run-1] == True:
                no_switch_wins += 1  
            no_switch_win_rates.append(no_switch_wins / run * 100)

        switch_win_rates = []
        switch_wins = 0
        for run in runs:
            if results_switch[run-1] == True:
                switch_wins += 1  
            switch_win_rates.append(switch_wins / run * 100)

        
        ax2.semilogx(runs, no_switch_win_rates, '-', color='#0C5DA5', alpha=0.8)
        ax2.semilogx(runs, switch_win_rates, '-', color='#00B438', alpha=0.8)
    
    ax2.semilogx([runs[0], runs[-1]], [1/3*100, 1/3*100], '--', color='#d3d3d3', alpha=0.7)
    ax2.semilogx([runs[0], runs[-1]], [2/3*100, 2/3*100], '--', color='#d3d3d3', alpha=0.7)
    ax2.set_xlabel('Simulation number')
    ax2.set_ylabel('Win rate (\%)')
    ax2.set_xlim(1, N)
    plt.legend(['Never switches', 'Always switches'])
    
    fig2.savefig('monty-hall-multiple.png', dpi=300, bbox_inches='tight')


if __name__ == '__main__':

    # Run N simulations where the contestant never switches doors
    results_no_switch = []
    for i in range(N):
        results_no_switch.append(simulate_game(switch=False))

    no_switch_wins = len([x for x in results_no_switch if x is True])
    no_switch_wins_rate = no_switch_wins / N * 100

    print(f"Never switches: {no_switch_wins} wins out of {N} games ({no_switch_wins_rate:.2f} % win rate).")


    # Run N simulations where the contestant always switches doors
    results_switch = []
    for i in range(N):
        results_switch.append(simulate_game(switch=True))

    switch_wins = len([x for x in results_switch if x is True])
    switch_wins_rate = switch_wins / N * 100

    print(f"Always switches: {switch_wins} wins out of {N} games ({switch_wins_rate:.2f} % win rate).")

    # Create plots
    plot_win_rate(results_no_switch, results_switch)

    run_multiple_sims(10)