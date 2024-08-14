This package is writting in python to connect to mongodb.

# Requirement_dev.txt we use for the testing.

It is easier to install and manage dependencies for development and testing seperate from the dependencies required for the productions

# Difference b/w requirement.txt and requirement_dev.txt .

requriments.txt is used to specify the dependencies required to run the
production code of a python projec, while requirements_dev.txt is used to specify the dependencies required for the development and testing purpose.

# tox.ini

We use it for the testing in the python package testing against different version of the python

# how tox works tox environmentcreation

1. Install dependencies and packages.
2. Run command
3. It is a combination of the (virtualenvwrapper and makefile)
4. It create a .tox

# pyproject.toml

it is being used for configuration the python project.It is the alternative of the setup.cfg file.
It contains configuration related to the build systems.
such as build tools package name version author license and dependencies.

# setup.cfg

In summery, setup.cfg is used by the setuptools to configure the packaging
and installation of a Python project.

# Testing the python application

type of testing

1. Manual Testing
2. Automation Testing

Mode of Testing

1. Unit Testing
2. Integrated Testing
