from setuptools import setup, find_packages

setup(
   name='osqu',
   version='0.1',
   description='A command-line interface tool to view the latest builds of openSUSE Tumbleweed from openQA',
   author='franjsco',
   author_email='',
   packages=find_packages(include=['osqu', 'osqu.*']),
   install_requires=[
       'colored==1.4.2',
       'tabulate==0.8.7',
       'requests-html==0.10.0'
    ],
   entry_points = {
        'console_scripts': ['osqu=osqu.osqu:main'],
    }
) 
