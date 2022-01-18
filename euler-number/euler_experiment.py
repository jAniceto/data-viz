import random
import math
from matplotlib import pyplot as plt


# Configuration
plt.style.use('science')
N = 100000


def pick_numbers_until_sum_one():
    sum_ = 0
    number_count = 0
    while sum_ < 1:
        number = random.uniform(0, 1)
        sum_ += number
        number_count += 1
    return number_count


numbers_needed = []
averages = []
deviations = []
for i in range(N):
    numbers_needed.append(pick_numbers_until_sum_one())
    avg = sum(numbers_needed) / len(numbers_needed)
    averages.append(avg)
    dev = (avg - math.e) / math.e * 100
    deviations.append(dev)

print(f"Average is {averages[-1]}")
print(f"Deviation is {deviations[-1]} %")

iterations = list(range(N))

fig, ax1 = plt.subplots()
ax1.plot(iterations, averages, '-')
ax1.plot([iterations[0], iterations[-1]], [math.e, math.e], '-')
ax1.set_xlabel('Simulation number')
ax1.set_ylabel('Average')
ax1.legend([
    f"Estimation ($e$ = {averages[-1]})", 
    "Euler's number ($e$ = 2.71828)"
])
fig.savefig('estimation_full.png', dpi=300, bbox_inches='tight')


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
fig2.savefig('estimation_10000.png', dpi=300, bbox_inches='tight')

plt.show()
