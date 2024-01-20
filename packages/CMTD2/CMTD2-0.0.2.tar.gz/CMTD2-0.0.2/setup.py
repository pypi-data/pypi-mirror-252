from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'CMTD functions'
LONG_DESCRIPTION = 'none.'

# Setting up
setup(
    name="CMTD2",
    version=VERSION,
    author="imemWassim",
    author_email="medimemhamdi18@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['matplotlib', 'networkx', 'numpy'],  # Corrected package names
    keywords=['python', 'markov', 'CMTD'],
    classifiers=[]
)
