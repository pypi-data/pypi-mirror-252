from setuptools import setup, find_packages
from combocmd.version import __version__

setup(
    name='aclustermap',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'seaborn',
        'colorcet',
        'pyarrow'
    ],
    entry_points={
        'console_scripts': [
            'aclustermap=aclustermap.aclustermap:main',
        ],
    },
    python_requires='>=3.6',
)
