def fibonacci_numbers(n):
    def fib(n):
        PHI = (1 + 5 ** 0.5) * 0.5
        return int((PHI ** n - (1 - PHI) ** n) / (2 * PHI - 1))
    return [fib(i) for i in range(n)]
