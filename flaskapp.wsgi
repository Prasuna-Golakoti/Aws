import sys
import os

sys.path.insert(0, "/var/www/html/flaskapp")
os.chdir("/var/www/html/flaskapp")

from flaskapp import app as application
