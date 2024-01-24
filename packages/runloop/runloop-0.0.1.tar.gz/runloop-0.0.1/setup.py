from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="runloop",
    version="0.0.1",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
)
