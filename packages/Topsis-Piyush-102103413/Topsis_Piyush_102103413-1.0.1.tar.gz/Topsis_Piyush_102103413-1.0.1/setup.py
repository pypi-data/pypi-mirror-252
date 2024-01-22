import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis_Piyush_102103413",
    version="1.0.1",
    description="Topsis_Piyush_102103413",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Piyush",
    author_email="ppiyush_be21@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=["numpy","pandas"],
   entry_points={
    'console_scripts': [
      'topsis=Topsis_Piyush_102103413.main:main',
    ],
  },
)