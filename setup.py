from setuptools import setup

setup(
    name='lyft-python',
    version='0.1.1',
    packages=['lyft', 'lyft.util', 'lyft.session',
              'lyft.authentication', 'tests'],
    url='https://github.com/vmanikes/Lyft-Python-SDK',
    license='',
    author='Raj Dutta',
    author_email='vmanikes@gmail.com',
    description='A simple python wrapper for Lyft REST API'
)
