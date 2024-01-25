from setuptools import setup, find_packages

setup(
    name='combocmd',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'combocmd=combocmd.combocmd',
        ],
    },
    python_requires='>=3.6',
)
