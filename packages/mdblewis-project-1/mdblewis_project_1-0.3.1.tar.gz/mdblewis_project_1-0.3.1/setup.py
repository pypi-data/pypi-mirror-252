from setuptools import setup, find_packages
import json

try:
    vers = json.load(open('version.json','r'))
    assert 'major' in vers and 'minor' in vers and 'patch' in vers
except Exception as e:
    vers = {'major':0,'minor':0,'patch':0}

vers['patch']+=1
verstr = str(vers['major'])+'.'+str(vers['minor'])+'.'+str(vers['patch'])
json.dump(vers,open('version.json','w'))

setup(
    name='mdblewis_project_1',
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


