#!/usr/bin/env python

"""
CI script for locating the improperly configured images.

Images that should trigger an error should be listed in
LIST_IMAGES variable.
"""

import sys
from logging import warning, error
from yaml import safe_load
from yaml.error import YAMLError
from git_root import git_root

FAIL_IMAGES = ['iroha2:dev']

def check_docker_config(config_file):
    status = 0
    services = {}
    try:
        with open(config_file, 'r', encoding='utf8') as config_contents:
            config_inst = safe_load(config_contents.read())
            if isinstance(config_inst, dict):
                services = config_inst.get('services', {})
            else:
                error(f'improper configuration at "{config_file}"')
                status = 1
    except YAMLError:
        error(f'improper formatting at "{config_file}"')
        status = 1
    for _, service in services.items():
        if service.get('image', '') in FAIL_IMAGES:
            status = 1
            break
    return status

def main():
    for yml_file in git_root().glob('*.yml'):
        if check_docker_config(yml_file):
            warning(f'wrong image in "{yml_file}"')
            sys.exit(1)
    print('Scan completed successfully')

if __name__ == '__main__':
    main()
