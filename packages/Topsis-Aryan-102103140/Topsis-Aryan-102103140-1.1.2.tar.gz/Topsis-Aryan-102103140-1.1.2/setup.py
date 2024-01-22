import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis-Aryan-102103140",
    version="1.1.2",
    description="Topsis-Aryan-102103140",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AryanGupta30/Topsis-Aryan-102103140.git",
    author="Aryan Gupta",
    author_email="30aryang@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["Topsis"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "Topsis=Topsis.__main__:main",
        ]
    },
)