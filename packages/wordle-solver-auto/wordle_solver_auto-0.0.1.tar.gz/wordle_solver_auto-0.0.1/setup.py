from setuptools import setup, find_packages

setup(
    name='wordle_solver_auto',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'selenium',
    ],
    entry_points={
        'console_scripts': [
            'wordle-solver-auto=wordle_solver_auto.solver:solv',
        ],
    },
)
