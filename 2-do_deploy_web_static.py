#!/usr/bin/python3

"""
Deploy archive to our remote web servers
"""

from fabric.api import *
from os import path
from datetime import datetime

env.user = "ubuntu"
env.hosts = ['34.224.1.147', '18.207.139.61']
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    Deploys an archive to the specified remote servers
    through ssh
    Attr:
        archive_path (str): The path of our compressed archive
    """
    try:
        if not (path.exists(archive_path)):
            return False

        # Upload the the archive to the /tmp directory of the server
        put(archive_path, '/tmp/')

        # Create the destination folder
        time_stamp = archive_path[-18:-4]
        run('mkdir -p /data/web_static/releases/web_static_{}/'.format
            (time_stamp))

        # Uncompress the archive to the web server
        run("tar -xzf /tmp/web_static_{}.tgz -C \
            /data/web_static/releases/web_static_{}/".format
            (time_stamp, time_stamp))

        # Delete the archive from the web server
        run('rm /tmp/web_static_{}.tgz'.format(time_stamp))

        # Delete the symbolic link from the web server
        run("mv /data/web_static/releases/web_static_{}/web_static/* \
            /data/web_static/releases/web_static_{}/".format
            (time_stamp, time_stamp))
        run("rm -rf /data/web_static/releases/web_static_{}/web_static"
            .format(time_stamp))
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s /data/web_static/releases/web_static_{}/ \
            /data/web_static/current".format(time_stamp))

        print("New Version deployed!")
    except Exception as e:
        return False

    return True
