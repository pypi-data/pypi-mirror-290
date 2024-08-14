from setuptools import setup, find_packages

setup(
    name="firewalla-api",
    version="0.1.1",
    author="Dan S",
    author_email="dan@d2digitalsolutions.com",
    description="Some functions for working with the FIrewalla API",
    long_description=open("README.md").read(),
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
