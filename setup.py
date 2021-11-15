from setuptools import setup, find_packages


with open('requirements.txt', 'r') as file:
    install_reqs = file.read().split("\n")
    file.close()

setup(
    install_requires=install_reqs,
    packages=find_packages(),
)
