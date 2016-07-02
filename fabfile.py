# -*- coding: utf-8 -*-

import re
import subprocess
from fabric.api import task
from fabric.api import local

from fabric.api import env
from fabric.api import sudo
from fabric.tasks import execute

env.use_ssh_config = True
env.roledefs = {
    'dev': ['mypre'],
}
env.roles = ['dev']


@task
def push():
    """
    Делает "git push --tags"
    """
    local('git push --tags')


@task
def upload():
    """
    Заливает новую версию в PyPi
    """
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
    Берет версию из git tag, увеличивает её и перезаписывает в setup.py.
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


@task
def make_new():
    """
    Зовёт inc_v, push и upload
    """
    execute(inc_v)
    execute(push)
    execute(upload)
