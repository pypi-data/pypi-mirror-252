from setuptools import setup, find_packages

setup(
    name='delete-copies',
    version='0.7',
    packages=find_packages(),
    install_requires=[
        'send2trash',
    ],
)
