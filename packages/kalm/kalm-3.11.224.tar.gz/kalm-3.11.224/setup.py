# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kalm',
 'kalm.airflow',
 'kalm.awx',
 'kalm.bump',
 'kalm.dns',
 'kalm.gitea',
 'kalm.inabox',
 'kalm.inthevault',
 'kalm.jenkins',
 'kalm.libvirt',
 'kalm.netbox',
 'kalm.netbox.terraform.cmdb',
 'kalm.pitv',
 'kalm.pypi',
 'kalm.semaphore',
 'kalm.ssh',
 'kalm.traefik',
 'kalm.ui',
 'kalm.ui.project',
 'kalm.ui.project.ignite',
 'kalm.ui.project.ignite.ansible',
 'kalm.ui.project.ignite.ansible.migrations',
 'kalm.ui.project.ignite.cmdb',
 'kalm.ui.project.ignite.cmdb.migrations',
 'kalm.ui.project.ignite.ignite',
 'kalm.ui.project.ignite.main',
 'kalm.ui.project.ignite.main.migrations',
 'kalm.ui.project.ignite.selinux',
 'kalm.ui.project.ignite.selinux.migrations',
 'kalm.vmware',
 'kalm.vmware.tools',
 'kalm.wireguard',
 'kalm.zabbix']

package_data = \
{'': ['*'],
 'kalm.netbox': ['terraform/terraform.d/*',
                 'terraform/terraform.d/plugins/registry.terraform.io/e-breuninger/netbox/3.7.5/linux_amd64/*'],
 'kalm.netbox.terraform.cmdb': ['data/*', 'modules/virtualmachine/*'],
 'kalm.ui.project.ignite': ['templates/*'],
 'kalm.ui.project.ignite.main': ['templates/*'],
 'kalm.ui.project.ignite.selinux': ['templates/*']}

install_requires = \
['GitPython>=3.1.41,<4.0.0',
 'PyYAML>=6.0.1,<7.0.0',
 'cryptography>=41.0.2,<42.0.0',
 'hvac>=1.1.0,<2.0.0',
 'mypy>=0.910,<0.911',
 'netbox>=0.0.2,<0.0.3',
 'paramiko>=3.3.1,<4.0.0',
 'pynetbox>=6.6.2,<7.0.0',
 'pytest>=6.2,<7.0',
 'python-jenkins>=1.7.0,<2.0.0',
 'pyvmomi>=8.0.2.0.1,<9.0.0.0',
 'redis>=4.5.3,<5.0.0',
 'requests>=2.25,<3.0',
 'toml>=0.10.2,<0.11.0',
 'xmltodict>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['kalm = kalm:main',
                     'kalm_airflow = kalm.airflow:main',
                     'kalm_bump = kalm.bump:main',
                     'kalm_dns = kalm.dns:main',
                     'kalm_gitea = kalm.gitea:main',
                     'kalm_inabox = kalm.inabox:main',
                     'kalm_jenkins = kalm.jenkins:main',
                     'kalm_libvirt = kalm.libvirt:main',
                     'kalm_netbox = kalm.netbox:main',
                     'kalm_pitv = kalm.pitv:main',
                     'kalm_semaphore = kalm.semaphore:main',
                     'kalm_ssh = kalm.ssh:main',
                     'kalm_traefik = kalm.traefik:main',
                     'kalm_vault = kalm.vault:main',
                     'kalm_vmware = kalm.vmware:main',
                     'kalm_zabbix = kalm.zabbix:main']}

setup_kwargs = {
    'name': 'kalm',
    'version': '3.11.224',
    'description': 'Knowit Automation lifecycle management',
    'long_description': None,
    'author': 'Jakob Holst',
    'author_email': 'jakob.holst@knowit.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://kalm.openknowit.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
