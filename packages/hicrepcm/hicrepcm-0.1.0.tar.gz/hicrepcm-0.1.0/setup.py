from setuptools import setup, find_packages

setup(
    name='hicrepcm',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'hicrep',
        'numpy',
        'matplotlib',
        'seaborn',
        'colorcet',
    ],
    entry_points={
        'console_scripts': [
            'hicrepcm=hicrepcm.hicrepcm:main',
        ],
    },
    python_requires='>=3.6',
)
