# https://www.youtube.com/watch?v=x1eaT88vJUA&list=LL&index=1&ab_channel=NeuralNine
import math


def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '#' * int(percent) + '-' * int(100 - int(percent))
    print(f"\rl{bar}| {percent:.2f}%", end="\r")


if __name__ == '__main__':
    numbers = [x * 5 for x in range(2000, 3000)]
    results = []

    progress_bar(0, len(numbers))
    for i, x in enumerate(numbers):
        results.append(math.factorial(x))
        progress_bar(i + 1, len(numbers))
