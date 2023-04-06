#!/usr/bin/python3
# Compresses before sending
"""
Generates a .tgz archive from contents of the web_static folder
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates .tgz archive and outputs its correct format
    """
    # Creates a folder if it doesn't exist hence the -p option
    local("mkdir -p versions")

    # Using the module datetime to format the name of the compressed file
    time_now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    # Defines the format in which the compressed file is saved
    saved_file = "versions/web_static_{}.tgz".format(time_now)
    # Defines the bash command to compress the contents
    comp_file = local("tar -cvzf {} web_static/".format(saved_file))

    if comp_file.failed:
        return None
    return(saved_file)
