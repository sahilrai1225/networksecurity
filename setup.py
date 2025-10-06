"""
The setup.py is an essential part of packaging and distributing Python Projects.
It is used by setuptools(or disutils in older python versions ) to define the configuration
of you project such as its metadata ,dependencies and more 
"""
from setuptools import find_packages,setup
from typing import List

## To get all requirement packages for projecct 
def get_requirements()->List[str]:
    """
    This function will return list of  requirements
    """
    
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            ## Read lines from the file
            lines=file.readlines()
            ## Process each line
            for line in lines:
                requirement=line.strip()  # to ignore empty spaces
                ## ignore empty line and -e .
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
        
    
    return requirement_lst


## setting up meta data
setup(
    name="Network Security",
    version="0.0.0.1",
    author="Sahil Rai",
    author_email="sahil.rai234234@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)