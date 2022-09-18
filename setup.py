from setuptools import find_packages, setup

setup(
    name='rpclib',
    packages=find_packages(include=['rpclib']),
    version='0.1.0',
    description='Remote process call library for inter process communication',
    author='ranoke',
    license='MIT',
    install_requires=[],
    setup_requires=[],
)