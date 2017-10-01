import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_uchiwa_installed(host):
    assert host.package('uchiwa').is_installed


def test_uchiwa_service(host):
    uchiwa = host.service('uchiwa')
    assert uchiwa.is_enabled
    assert uchiwa.is_running


def test_uchiwa_listening(host):
    assert host.socket('tcp://0.0.0.0:3000').is_listening


def test_uchiwa_config(host):
    config = host.file('/etc/sensu/uchiwa.json')
    assert config.exists
    assert config.is_file
    assert config.user == 'uchiwa'
    assert config.group == 'uchiwa'
    assert config.mode == 0o600
    assert config.contains('"name": "Site 1"')
