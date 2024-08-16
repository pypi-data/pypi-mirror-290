"""Restarts apxlet if version does not match"""

import os
import subprocess

from apx.apxlet import constants

VERSION_FILE = os.path.expanduser(constants.APXLET_VERSION_FILE)


def restart_apxlet():
    # Kills old apxlet if it is running.
    # TODO(zhwu): make the killing graceful, e.g., use a signal to tell
    # apxlet to exit, instead of directly killing it.
    subprocess.run(
        # We use -m to grep instead of {constants.APX_PYTHON_CMD} -m to grep
        # because need to handle the backward compatibility of the old apxlet
        # started before #3326, which does not use the full path to python.
        'ps aux | grep "apx.apxlet.apxlet" | grep " -m "'
        '| awk \'{print $2}\' | xargs kill >> ~/.apx/apxlet.log 2>&1',
        shell=True,
        check=False)
    subprocess.run(
        # We have made sure that `attempt_apxlet.py` is executed with the
        # apxdeploy runtime env activated, so that apxlet can access the cloud
        # CLI tools.
        f'nohup {constants.APX_PYTHON_CMD} -m apx.apxlet.apxlet'
        ' >> ~/.apx/apxlet.log 2>&1 &',
        shell=True,
        check=True)
    with open(VERSION_FILE, 'w', encoding='utf-8') as v_f:
        v_f.write(constants.APXLET_VERSION)


proc = subprocess.run(
    'ps aux | grep -v "grep" | grep "apx.apxlet.apxlet" | grep " -m"',
    shell=True,
    check=False)

running = (proc.returncode == 0)

version_match = False
found_version = None
if os.path.exists(VERSION_FILE):
    with open(VERSION_FILE, 'r', encoding='utf-8') as f:
        found_version = f.read().strip()
        if found_version == constants.APXLET_VERSION:
            version_match = True

version_string = (f' (found version {found_version}, new version '
                  f'{constants.APXLET_VERSION})')
if not running:
    print('Apxlet is not running. Starting (version '
          f'{constants.APXLET_VERSION})...')
elif not version_match:
    print(f'Apxlet is stale{version_string}. Restarting...')
else:
    print(
        f'Apxlet is running with the latest version {constants.APXLET_VERSION}.'
    )

if not running or not version_match:
    restart_apxlet()
