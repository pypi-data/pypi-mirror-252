import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="packageinit",
    version="1.0",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/yannikkellerde/packageinit",
    author="Yannik Keller",
    author_email="yannik@kelnet.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["packageinit"],
    include_package_data=True,
    entry_points={
        "console_scripts": ["packageinit=packageinit.packageinit:command_line_run"]
    },
)
