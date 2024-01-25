from setuptools import setup, find_packages

setup(
    name="list-to-tabs",
    version="1.2.2",
    #version="2.0.1",
    description="A python package for converting newline files into konsole-tabs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jackpots28/list_to_konsole-tabs",
    author="Jack Sims",
    author_email="jack.m.sims@protonmail.com",
    license="GPL",
    packages=find_packages(),
    install_requires=[
        "argparse",
        "setuptools",
        "wheel",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": ["list-to-tabs=src.main:main"],
    },
)
print(find_packages())
