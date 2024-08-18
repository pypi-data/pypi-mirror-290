from setuptools import setup, find_packages

setup(
    name='blackwhite',
    version='0.1.1',
    author='Vemy',
    author_email='chessom@foxmail.com',
    description='BlackWhite bindings with Python',
    long_description='This module includes color, board, and moves for the BlackWhite game.',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['bw.pyd']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
