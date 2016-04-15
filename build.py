import os

from pybuilder.core import init, use_plugin
from pybuilder.vcs import VCSRevision


use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin('python.cram')
use_plugin('pypi:pybuilder_aws_plugin')

name = "ec2-terminate-wailt"
summary = '(de)activates the terminate-wait livecycle hook on a ec2 instance'
description = """
"""
license = 'Apache License 2.0'
url = 'https://github.com/ImmobilienScout24/aws-ec2-terminate-wait'
version = '%s.%s' % (VCSRevision().get_git_revision_count(), os.environ.get('BUILD_NUMBER', '0'))
default_task = ['clean', 'analyze', 'package']


@init
def set_properties(project):
    project.build_depends_on('unittest2')
    project.build_depends_on('requests_mock')
    project.build_depends_on('mock')
    project.build_depends_on('coverage')
    project.build_depends_on('moto')
    project.build_depends_on('docopt')

    project.depends_on('boto3')
    project.depends_on('requests')
    project.depends_on('sh')
    project.depends_on('cfn-sphere')

    project.set_property('bucket_name', os.environ.get('BUCKET_NAME_FOR_UPLOAD', 'sns-subscription-distribution'))

    project.set_property('template_files', [('templates', '%s.yml' % project.name)])

    project.set_property('copy_resources_target', '$dir_dist')
    project.set_property('install_dependencies_upgrade', True)


@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    project.set_property('teamcity_output', True)
    project.set_property('install_dependencies_index_url', os.environ.get('PYPIPROXY_URL'))
