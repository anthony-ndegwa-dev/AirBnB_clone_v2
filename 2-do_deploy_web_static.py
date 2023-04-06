#!/usr/bin/env python3
""" Fabric script (based on the file 1-pack_web_static.py)
    that distributes an archive to your web servers """
from fabric.api import *
import os.path


env.hosts = ['<34.234.193.7>', '<54.174.67.136>']


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""

    if not os.path.isfile(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder
        archive_filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_filename)[0]
        run("sudo mkdir -p /data/web_static/releases/{}/"
                .format(archive_name))
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
                .format(archive_filename, archive_name))

        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(archive_filename))

        # Move files from archive to the right path
        run("sudo mv /data/web_static/releases/{}/web_static/*
                /data/web_static/releases/{}/".
                format(archive_name, archive_name))
        run("sudo rm -rf /data/web_static/releases/{}/web_static".
                format(archive_name))

        # Delete the symbolic link /data/web_static/current from web server
        run("sudo rm -rf /data/web_static/current")

        # Create new symbolic link /data/web_static/current on the web server
        run("sudo ln -s /data/web_static/releases/{}/
                /data/web_static/current".format(archive_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Error: {}".format(e))
        return False

