from typing import List
from setuptools import find_packages, setup

HYPHEN_E = '-e .'

def get_requirements(file_path: str)-> List[str]:
    '''
    This function will return a list.
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n", "") for req in requirements]

        if HYPHEN_E in requirements:
            requirements.remove(HYPHEN_E)




setup(
    name='blog-site',
    version='0.0.1',
    author='1666sapple',
    author_email='ananno.034@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
