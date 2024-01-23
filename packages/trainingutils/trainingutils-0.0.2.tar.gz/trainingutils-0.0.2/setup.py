from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Training tools for Deep Learning'
LONG_DESCRIPTION = 'A python package to assist developers to be more efficient at their own models'

# Setting up
setup(
    name="trainingutils",
    version=VERSION,
    author="Michael-Holland-Dev (Michael Holland)",
    author_email="<michael.w.holland@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'pandas',
        'torch',
        'torchvision',
        'matplotlib',
        'diffusers',
        'tqdm',
    ],
    keywords=[
        'artificial intellgience',
        'machine learning',
        'computer vision',
        'deep learning'
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)