from setuptools import setup, find_packages
setup(
    name='paddycmd',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'easygui',
        'argparse'
                      ],
    entry_points={
        'console_scripts': [
            'paddy = paddycmd:main',
        ],
    },
)