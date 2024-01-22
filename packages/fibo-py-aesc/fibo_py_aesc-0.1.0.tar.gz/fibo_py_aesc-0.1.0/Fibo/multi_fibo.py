from .fibo import fibo


def multi_fibo(nums):
    return [fibo(num) for num in nums]
