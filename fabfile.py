# -*- coding: utf-8 -*-

import re
import subprocess
from fabric.api import task
from fabric.api import local

from fabric.api import env
from fabric.api import sudo
from fabric.contrib.project import rsync_project

env.use_ssh_config = True
env.roledefs = {
    'dev': ['mypre'],
}
env.roles = ['dev']


@task
def up():
    excludes = ('.DS_Store', '*.pyc', '._*',
                '.env', 'settings_local.py',
                'media', 'coffee', '.svn', '.git')
    rsync_project('/home/drmartiner/pixelgold/src/', './yandex_kassa', exclude=excludes)
    sudo('service uwsgi restart pixelgold')


@task
def push():
    local('git push')


@task
def upload():
    local('python setup.py sdist upload')


def get_last_version_from_tags():
    versions = subprocess.check_output(["git", "tag"])
    versions = versions.split('\n')
    version_regex = re.compile('(\d+)\.(\d+)\.(\d+)')
    versions = [map(int, v.split('.')) for v in versions if version_regex.match(v)]
    versions.sort(reverse=True)
    return versions[0]


@task
def inc_v():
    """
    Increase the version
    """
    if 'nothing to commit' not in subprocess.check_output(["git", "status"]):
        print 'Error: You must commit current changes first'
        return

    last_version = get_last_version_from_tags()
    with open('setup.py', 'r') as file:
        setup_py = file.read()

    new_version = last_version[:]
    new_version[2] += 1
    last_version = '.'.join(map(str, last_version))
    new_version = '.'.join(map(str, new_version))

    print 'Upgrading from %s to %s' % (last_version, new_version)

    version_line_re = re.compile(r'''(__version__ =)(\s*['"]\d+\.\d+\.\d+["'])''', flags=re.M)
    with open('setup.py', 'w') as f:
        f.write(version_line_re.sub('\\1 "%s"' % new_version, setup_py))

    subprocess.check_output(["git", 'commit', '-m', '"version %s"' % new_version, '-a'])
    subprocess.check_output(["git", 'tag', '%s' % new_version])

    print '\nVersion %s created. Push it to origin with "git push --tags"' % new_version
