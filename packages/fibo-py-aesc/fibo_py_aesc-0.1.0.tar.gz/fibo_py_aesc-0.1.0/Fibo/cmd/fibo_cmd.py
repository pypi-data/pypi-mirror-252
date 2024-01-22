import argparse

from Fibo import fibo


def fibo_calc():
    parser = argparse.ArgumentParser(
            description="Calculate Fibonacci Number")
    parser.add_argument(
            "--number",
            action="store",
            type=int,
            required=True,
            help="Input to the fibonacci calculation")

    args = parser.parse_args()
    print(f"fibonacci({args.number}) = {fibo(args.number)}")
