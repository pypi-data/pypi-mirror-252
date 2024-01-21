metaData={"major": 0, "minor": 0, "patch": 11, "projName": "mdblewisProj1"}

from setuptools import setup, find_packages
import json

verstr = str(metaData['major'])+'.'+str(metaData['minor'])+'.'+str(metaData['patch'])


setup(
    name=metaData['projName'],
    version=verstr,
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author='mdblewis',
    author_email='mdblewis@protonmail.com',
    description='a test project',
    url='https://github.com/mathewdblewis/testingPyPi',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)


