from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """This function installs the required packages for the project

    Returns:
        List[str]: _description_
    """
    try:
        requried_list = []
        with open('requirements.txt') as f:
            lines =  f.readlines()
            for line in lines:
                requriments = line.split()
                if requriments and requriments != "-e .":
                    requried_list.append(requriments[0])
       
    except Exception as e:
        print(f"Error: {e}")
        return requried_list
    
    return requried_list

# print(get_requirements())

setup(
    name = "networksecurity",
    version="0.0.1",
    author= "sadhiin",
    packages=find_packages(),
    install_requires=get_requirements(),
)