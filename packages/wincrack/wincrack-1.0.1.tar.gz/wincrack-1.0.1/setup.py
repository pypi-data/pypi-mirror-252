from setuptools import setup, find_packages

setup(
    name='wincrack',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'pystyle',
    ],
    entry_points={
        'console_scripts': [
            'wincrack = WinCrack.WinCrack:main',
        ],
    },
)