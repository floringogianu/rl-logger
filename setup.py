from setuptools import setup, find_packages

setup(
    name='rl_logger',
    version='0.1',
    description='A simple logger for reinforcement learning.',
    url='https://github.com/floringogianu/rl_logger',
    author='Florin Gogianu',
    author_email='florin.gogianu@gmail.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'termcolor==1.1.0'
    ],
)
