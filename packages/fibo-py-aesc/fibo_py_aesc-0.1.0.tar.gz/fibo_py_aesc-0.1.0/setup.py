from setuptools import find_packages, setup

with open("README.md") as fhandle:
    long_description = fhandle.read()

setup(
    name="fibo_py_aesc",
    version="0.1.0",
    author="Abraham Escalante",
    description="Calculates a Fibonacci Number",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/aeklant/fibo.git",
    install_requires=[],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "fibonacci = Fibo.cmd.fibo_cmd:fibo_calc",
        ]
    },
)
