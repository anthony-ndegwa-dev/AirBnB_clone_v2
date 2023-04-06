#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers using the function do_deploy:

    Prototype: def do_deploy(archive_path):
    Returns False if the file at the path archive_path doesn’t exist
    The script should take the following steps:
        Upload the archive to the /tmp/ directory of the web server
        Uncompress the archive to the folder
          /data/web_static/releases/<archive filename without extension>
          on the web server
        Delete the archive from the web server
        Delete the symbolic link /data/web_static/current from the web server
        Create a new symbolic link /data/web_static/current on the web server,
          linked to the new version of your code
          (/data/web_static/releases/<archive filename without extension>)
    All remote commands must be executed on your both web servers:
      (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
    Returns True if all operations are done correctly, otherwise returns False
    You must use this script to deploy it on your servers:
      xx-web-01 and xx-web-02
"""
from datetime import datetime
from fabric.api import *
import shlex
import os


env.hosts = ['34.234.193.7', '54.174.67.136']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """ Deploys archives to the web servers """
    if not os.path.exists(archive_path):
        return False
    try:
        name = archive_path.replace('/', ' ')
        name = shlex.split(name)
        name = name[-1]

        wname = name.replace('.', ' ')
        wname = shlex.split(wname)
        wname = wname[0]

        releases_path = "/data/web_static/releases/{}/".format(wname)
        tmp_path = "/tmp/{}".format(name)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}web_static".format(releases_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(releases_path))
        print("New version deployed!")
        return True
    except:
        return False
