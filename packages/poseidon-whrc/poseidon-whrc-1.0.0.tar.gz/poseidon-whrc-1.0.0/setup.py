from setuptools import setup, find_packages

setup(
    name='poseidon-whrc',
    version='1.0.0',
    author='Ioannis Christodoulakis',
    author_email='ioannis.ch@outlook.com',
    description='Wireless Handheld Remote Controller',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)