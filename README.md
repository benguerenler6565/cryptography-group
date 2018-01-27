# Group 3 Cryptography

## Installation

This program is written in Python 3.6 (3.5 compatible).
Package library requirements are contained in requirement.txt
It is recommennded to create a virtual envirnoment and install the requirements with pip:
 
$ pip install -r requirements.txt
 
## Execution
 
Program execution is performed by running the command:
 
$ python operations.py 
 
## On Siegbahn Ubuntu Remote Server (with pip, virtualenv and Python3.5 pre-installed)

$ ssh "username"@siegbahn.it.uu.se

$ git clone https://github.com/attack68/cryptography-group.git

$ virtualenv --python=python3.5 CryptoVenv

$ source CryptoVenv/bin/activate

$ cd cryptography-group

$ pip install -r requirements.txt

$ python operations.py