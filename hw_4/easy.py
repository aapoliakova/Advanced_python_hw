from multiprocessing import Process
from threading import Thread
from timeit import timeit


def f(n: int = 1e6):
    assert n >= 0
    f0, f1 = 0, 1
    first_n = [f0, f1]
    for _ in range(n - 2):
        f0, f1 = f1, f0 + f1
        first_n.append(f1)
    return first_n[:n]


def function_jobs(engine, n, num_jobs=10):
    jobs = []
    for _ in range(num_jobs):
        jobs.append(engine(target=f, args=(n,)))
        jobs[-1].start()

    for job in jobs:
        job.join()


def sequential(n, k):
    return timeit(lambda: f(n), number=k)


def threading(n, k):
    return timeit(lambda: function_jobs(Thread, n), number=k)


def multiprocessing(n, k):
    return timeit(lambda: function_jobs(Process, n), number=k)


if __name__ == "__main__":
    n = int(1e5)
    k = 10

    with open("artifacts/easy.txt", "w+") as file:
        file.write(f"n = {n}\n")
        file.write(f"sequential timeit with {k} runs: {sequential(n, k)} s.\n")
        file.write(f"threading timeit with {k} runs: {threading(n, 1)} s.\n")
        file.write(f"multiprocessing timeit with {k} runs: {multiprocessing(n, 1)} s.\n")
