import sys

# add project directory to the sys.path
sys.path.insert(0, '/home/chase/PycharmProjects/11.14.23.API/venv')

#import app
from app import app as application

import sys

# Path to the directory where app.py is located
project_home = '/home/chase/PycharmProjects/11.14.23.API/'

# Path to the virtual environment's site-packages, if you're using a virtual environment
activate_this = '/home/chase/PycharmProjects/11.14.23.API/venv/lib/python3.10/site-packages'

sys.path.insert(0, project_home)
sys.path.insert(1, activate_this)

from app import app as application
