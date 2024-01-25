from setuptools import setup, find_packages

setup(
    name='combocmd',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'combocmd=combocmd.combocmd:main',
        ],
    },
    python_requires='>=3.6',
)
