import sys

# path to the venv
sys.path.insert(0, '/home/chase/PycharmProjects/11.14.23.API/venv')

# path to the project directory
project_home = '/home/chase/PycharmProjects/11.14.23.API/'
sys.path.insert(1, project_home)

# path to the venv site-packages
activate_this = '/home/chase/PycharmProjects/11.14.23.API/venv/lib/python3.10/site-packages'
sys.path.insert(2, activate_this)

# import the app
from app import app as application
