from setuptools import setup

setup(
    name='chess_engine',
    version='0.1',
    py_modules=['engine'],
    install_requires=[
        # only the standard python libraries.
    ],
    entry_points={
        'console_scripts': [
            'chess-engine=engine:main',  # Assumes your entry point function is `main`
        ],
    },
    description='A simple UCI-compliant chess engine',
    author='Vansh Talyani',
    author_email='vanshtalyani12@gmail.com',
    url='https://github.com/VANSHTalyani/chess_game',  
)
