import os
from setuptools import setup, find_packages


PACKAGE_NAME = "naplib"
DESCRIPTION = "Tools and functions for neural data processing and analysis in python"
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()
AUTHOR = "Gavin Mischler, Vinay Raghavan, Menoua Keshishian"
MAINTAINER = "Gavin Mischler"
MAINTAINER_EMAIL = "gm2944@columbia.edu"
URL = "https://github.com/naplab/naplib-python"
PYTHON_VERSION = '>=3.8'  # Minimum Python version
with open("./requirements.txt", "r") as f:
    REQUIRED_PACKAGES = f.read()

# Find package version.
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
for line in open(os.path.join(PROJECT_PATH, "naplib", "__init__.py")):
    if line.startswith("__version__ = "):
        VERSION = line.strip().split()[2][1:-1]

non_python_files = ['features/*.mat',
                    'features/eng.*',
                    'features/prosodylab_aligner/eng.*',
                    'features/resample.sh',
                    'features/prosodylab_aligner/LICENSE',
                    'features/test.wav',
                    'io/sample_data/*.mat',
                    'visualization/*.locs'
                    ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    install_requires=REQUIRED_PACKAGES,
    python_requires=PYTHON_VERSION,
    url=URL,
    project_urls={
      'Source': URL,
      'Tracker': URL + '/issues/',
    },
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    packages=find_packages(),
    package_data={'naplib': non_python_files},
    include_package_data=True,
)
