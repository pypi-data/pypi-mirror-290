from setuptools import setup, find_packages

setup(
    name="AnkurKnapsack",
    version="1.0",
    packages=find_packages(),
    description="A package for solving the Fractional Knapsack problem using a greedy approach",
    author="Ankur Ahire",
    author_email="ankurahire6@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
