from setuptools import setup, find_packages
import json

try:
    metaData = json.load(open('metaData.json','r'))
    assert 'major' in vers and 'minor' in vers and 'patch' in vers and 'projName' in vers
except Exception as e:
    projName = input('project name: ')
    metaData = {'major':0,'minor':0,'patch':0,'projName':projName}

metaData['patch']+=1
verstr = str(metaData['major'])+'.'+str(metaData['minor'])+'.'+str(metaData['patch'])
json.dump(metaData,open('metaData.json','w'))

setup(
    name=metaData['projName'],
    version=verstr,
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author='mdblewis',
    author_email='mdblewis@protonmail.com',
    description='a test project',
    url='https://github.com/mathewdblewis/testingPyPi',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)


