"""
Setup file for auth_utils package
"""
from setuptools import setup, find_packages

setup(
    name='auth-vpetrov',
    version='0.2.2',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'user-vpetrov',
        'typing'
    ],
)
