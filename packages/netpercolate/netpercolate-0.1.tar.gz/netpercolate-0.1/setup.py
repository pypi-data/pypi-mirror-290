from setuptools import setup, find_packages

setup(
    name="netpercolate",
    version="0.1",
    author="Justin Yeung",
    author_email="jyeungnl@gmail.com",
    description="A simple python package for targeted percolation in social networks",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pandas == 2.2.2',
        'networkx == 3.3',
        'numpy == 1.22.4'
        ]
)