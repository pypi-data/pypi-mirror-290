# setup.py

from setuptools import setup, find_packages

setup(
    name='JsonGrabber',
    version='0.1',
    packages=find_packages(),
    description='A utility library for extracting JSON from text strings',
    author='YEVHRAFOV Artem',
    author_email='all@power-display.com',
    url='https://github.com/artyomevgrafov/JsonGrabber',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
