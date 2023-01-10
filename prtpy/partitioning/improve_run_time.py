import time
import concurrent.futures
from prtpy.partitioning import Horowitz_And_Sahni
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import Schroeppel_Shamir

WORKERS = 4


# improve by thread
def threads():
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        executor.submit(Horowitz_And_Shani)
    print(f"{WORKERS} threads: time={time.perf_counter() - start} seconds")
    return time.perf_counter() - start


# improve by thread, ss algorithm
def threads2():
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        executor.submit(Schroeppel_Shamir)
    print(f"{WORKERS} threads of ss algorithm: time={time.perf_counter() - start} seconds")
    return time.perf_counter() - start


# base, without the improvement
def run_time():
    start_time = time.perf_counter()
    Horowitz_And_Shani
    print("the time without thread use is: ", time.perf_counter() - start_time, "seconds")
    return time.perf_counter() - start_time


# base, without the improvement, ss
def run_time2():
    start_time = time.perf_counter()
    Schroeppel_Shamir
    print("ss algorithms, the time without thread use is: ", time.perf_counter() - start_time, "seconds")
    return time.perf_counter() - start_time


def print_graph():
    # plt.xlabel('time')
    # # plt.ylabel('size')
    # plt.title('compare run times: ')
    # x = np.array([2, 4, 6, 8, 10])
    #
    # # plt.plot(threads(), label='line 1')
    # # plt.plot(run_time(), label='line 2')
    #
    # plt.plot(x, threads(), color="red", label="threads")
    # # plt.plot(x, run_time(), marker='+', linestyle='-', label='runtime')
    # plt.legend(loc="upper left")
    #
    # # plt.legend()
    # plt.show()

    x = time.perf_counter()
    y = threads()
    z = run_time()
    w = threads2()
    v = run_time2()
    plt.title('compare run times:')
    plt.xlabel('time')
    plt.ylabel('size')
    plt.plot(x, y, color="red", linewidth=1.5, linestyle="-.", label="threads")
    plt.plot(x, z, linestyle='-', label='base')
    plt.plot(x, w, linestyle='-', label='threads2')
    plt.plot(x, v, linestyle='-', label='base_ss')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    threads()
    print("-------------------")
    run_time()
    print("-------------------")
    threads2()
    print("-------------------")
    run_time2()
    print("-------------------")
    print_graph()
