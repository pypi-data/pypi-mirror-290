from setuptools import setup, find_packages

setup(
    name="LoggoBlocks",
    version="0.1",
    packages=find_packages("loggoblocks"),
    install_requires=["pyyaml"],
    python_requries=">=3.0",
    author="Brian Towner",
    author_email="briantwnr47@gmail.com",
    description="Logging abstraction",
    url="https://github.com/MoronicGoat/loggoblocks.git",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)