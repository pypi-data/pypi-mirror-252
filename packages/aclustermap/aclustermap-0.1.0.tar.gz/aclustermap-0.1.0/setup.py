from setuptools import setup, find_packages

setup(
    name='aclustermap',
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
            'aclustermap=aclustermap.aclustermap:main',
        ],
    },
    python_requires='>=3.6',
)
