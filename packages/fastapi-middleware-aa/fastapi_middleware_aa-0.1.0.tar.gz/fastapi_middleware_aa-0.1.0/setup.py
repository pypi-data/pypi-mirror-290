# setup.py

from setuptools import setup, find_packages

setup(
    name='fastapi-middleware-aa',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'starlette'
    ],
    description='A FastAPI middleware example',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/fastapi-middleware-aa',
)