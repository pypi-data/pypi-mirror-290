from setuptools import setup, find_packages
from typing import List 


"""
HYPEN_E_DOT ="-e."
file_name='requirements_dev.txt'
file_path=os.path.join(ROOT_DIR,file_name)

def get_requirements(file_path:str):
  requirements=[]
  with open(file_path) as f:
    requirements=f.readlines()
    requirements=[req.replace("\n","") for req in requirements]
    if HYPEN_E_DOT in requirements:
      requirements.remove(HYPEN_E_DOT)
  return requirements
"""




long_descriptions="This package is build to automate the Mongodb CRUD operation"   
    


   

__version__ = "0.0.1"
REPO_NAME = "mongodbconnectorpkg"
PKG_NAME= "mongodbautomationpackage"
AUTHOR_USER_NAME = "prashant0708"
AUTHOR_EMAIL = "prashantsingh.aiengineer@gmail.com"

setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A python package for connecting with database.",
    long_description=long_descriptions,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    )