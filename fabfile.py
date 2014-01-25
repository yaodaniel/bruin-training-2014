from __future__ import with_statement

import os
import sys
import time
import random
from fabric.api import *
from os.path import expanduser

pwd = os.path.dirname(__file__)
sys.path.append(pwd)


#
# Local operations
#


def generate_secret(length=50,
    allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'):
    """
    Generates secret key for use in Django settings.
    """
    key = ''.join(random.choice(allowed_chars) for i in range(length))
    print 'SECRET_KEY = "%s"' % key


def rmpyc():
    """
    Erases pyc files from current directory.

    Example usage:

        $ fab rmpyc

    """
    print("Removing .pyc files")
    with hide('everything'):
        local("find . -name '*.pyc' -print0|xargs -0 rm", capture=False)


def rs(port=8000):
    """
    Fire up the Django test server, after cleaning out any .pyc files.

    Example usage:
    
        $ fab rs
        $ fab rs:port=9000
    
    """
    with settings(warn_only=True):
        rmpyc()
    local("python manage.py runserver 0.0.0.0:%s" % port, capture=False)


def sh():
    """
    Fire up the Django shell, after cleaning out any .pyc files.

    Example usage:
    
        $ fab sh
    
    """
    rmpyc()
    local("python manage.py shell", capture=False)


def tabnanny():
    """
    Checks whether any of your files have improper tabs
    
    Example usage:
    
        $ fab tabnanny
    
    """
    print("Running tabnanny")
    with hide('everything'):
        local("python -m tabnanny ./")


def pep8():
    """
    Flags any violations of the Python style guide.

    Requires that you have the pep8 package installed

    Example usage:

        $ fab pep8

    Documentation:

        http://github.com/jcrocholl/pep8

    """
    print("Checking Python style")
    # Grab everything public folder inside the current directory
    dir_list = [x[0] for x in os.walk('./') if not x[0].startswith('./.')]
    # Loop through them all and run pep8
    results = []
    with hide('everything'):
        for d in dir_list:
            results.append(local("pep8 %s" % d))
    # Filter out the empty results and print the real stuff
    results = [e for e in results if e]
    for e in results:
        print(e)


def big_files(min_size='20000k'):
    """
    List all files in this directory over the provided size, 20MB by default.
    
    Example usage:
    
        $ fab big_files
    
    """
    with hide('everything'):
        list_ = local("""find ./ -type f -size +%s -exec ls -lh {} \; | awk '{ print $NF ": " $5 }'""" % min_size)
    if list_:
        print("Files over %s" % min_size)
        print(list_)
    else:
        print("No files over %s" % min_size)