"""
setup guide = https://packaging.python.org/en/latest/tutorials/packaging-projects/
markdown guide = https://www.markdownguide.org/cheat-sheet/
"""

from setuptools import setup, find_packages

setup(
    name='newearthquake-BMKG',
    version='0.2',
    packages=find_packages(),
    install_requires=[],
    author='Lukas Yulianto',
    author_email='paten26@gmail.com',
    description='This package get the last update earthquake from BMKG Indonesia',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/paten26/BMKG_latest_earthquake',  # URL repositori
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
