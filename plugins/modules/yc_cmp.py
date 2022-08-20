#!/usr/bin/python3

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: yc

short_description: Yandex Cloud instance controller

version_added: "1.0.0"

description: This module translate commands to Yandex Cloud CLI in order to control instances

options:
    machine:
        description: name of the instance
        required: true
        type: str
    config:
        description: instance configuration
        required: True
        type: dict
    state:
        description: state of the instance
        required: false
        type: str
        default: 'exists'



extends_documentation_fragment:
    - artem_shtepa.utils.yc

author:
    - Artem Shtepa
'''

EXAMPLES = r'''
- name: Create YC instance
  artem_shtepa.utils.yc:
    machine: "my-centos-7"
    config:
      core-fraction: 5
      cores: 2
      memory: 1GB
      create-boot-disk:
        size: 20GB
        image-folder-id: standard-images
        image-family: centos-8
      public-ip: true
      ssh-key: "~/.ssh/id_ed25519.pub"
- name: Destroy YC instance
  artem_shtepa.utils.yc:
    machine: centos_7
    state: absent
'''

RETURN = r'''
version:
    description: Yandex.Cloud CLI version
    type: str
    returned: always
    sample: 'Yandex Cloud CLI 0.93.0 linux/amd64'
config:
    description: Instance configuration from Yandex.Cloud CLI
    type: str
    returned: if instance if exists or created
ip:
    description: External IP address of the YC instance
    type: str
    returned: if state is "exists"
    sample: '77.88.8.8'
'''

from ansible.module_utils.basic import AnsibleModule
import os, subprocess, json


update_allowed = ['cores','core-fraction','memory']


def get_oneline_param(cmd):
    p = subprocess.run(cmd, capture_output=True, encoding='utf-8', shell=True)
    return int(p.returncode), str(p.stdout.replace('\n','')), str(p.stderr)


def build_cmd_line(params):
    cmd = ''
    for p in params:
        buf = ''
        v = params[p]
        if type(v) == bool:
            if v != True:
                p = ''
        elif type(v) == dict:
            for p2 in v:
                if buf != '':
                    buf += ','
                if v[p2].find(' ') >= 0:
                    buf += p2+'="'+v[p2]+'"'
                else:
                    buf += p2+'='+v[p2]
        else:
            buf = str(v)
        if p != '':
            if cmd != '':
                cmd += ' '
            cmd += '--'+str(p)
            if buf != '':
                cmd += ' '+buf
    return cmd


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        machine=dict(type='str', required=True),
        config=dict(type='dict', required=True),
        state=dict(type='str', required=False, default='exists')
    )

    result = dict(
        changed=False
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    yc_auth = dict()

    #Check YC CLI availability
    res = get_oneline_param('yc --version')
    if res[0] != 0:
        module.fail_json(msg='Can`t run YandexCloud CLI. Check https://cloud.yandex.ru/docs/cli/operations/install-cli', **result)
    else:
        result['version'] = res[1]

    #Verify YC CLI authorizaion
    for param in ['token', 'cloud-id', 'folder-id', 'compute-default-zone']:
        res = get_oneline_param('yc config get '+param)
        if res[0] != 0:
            module.fail_json(msg='Can`t get config param `'+param+'`. Check YC CLI authorization by `yc init`', **result)
        else:
            yc_auth[param] = res[1]

    if not 'zone' in module.params['config']:
        module.params['config']['zone'] = yc_auth['compute-default-zone']

    res = get_oneline_param('yc compute instance get '+module.params['machine']+' --format=json')
    if res[0] != 0:
        # Instance not found
        if module.params['state'] == 'absent':
            # Nothing to do
            module.exit_json(**result)
        else:
            # Create new instance
            result['yc_args'] = build_cmd_line(module.params['config'])
            res = get_oneline_param('yc compute instance create '+module.params['machine']+' '+build_cmd_line(module.params['config'])+' --format=json')
            if res[0] != 0:
                module.fail_json(msg=res[2], **result)
            result['config'] = json.loads(res[1])
            result['changed'] = True
    else:
        result['config'] = json.loads(res[1])
        # Instance is found
        if module.params['state'] == 'absent':
            # Destroy instance
            res = get_oneline_param('yc compute instance delete '+module.params['machine'])
            if res[0] != 0:
                module.fail_json(msg=res[2], **result)
            result['changed'] = True
        else:
            # Update instance - can be modified only cores, core-fraction and memory
            upd_params = dict()
            for p in update_allowed:
                if p in module.params['config']:
                    upd_params[p] = module.params['config'][p]
            # Check update needless
            need_update = False
            if str(upd_params['cores']) != result['config']['resources']['cores']:
                need_update = True
            if str(upd_params['core-fraction']) != result['config']['resources']['core_fraction']:
                need_update = True
            cnf_mem = upd_params['memory']
            if cnf_mem.find('GB') != -1:
                cnf_mem = int(cnf_mem.replace('GB',''))*1024*1024*1024
            if str(cnf_mem) != result['config']['resources']['memory']:
                need_update = True
            # Update if needed
            if need_update:
                # Build CLI command
                result['yc_args'] = build_cmd_line(upd_params)
                # Stop instance if RUNNING
                if result['config']['status'] == 'RUNNING':
                    res = get_oneline_param('yc compute instance stop '+module.params['machine'])
                    if res[0] != 0:
                        module.fail_json(msg=res[2], **result)
                # Update instance
                res = get_oneline_param('yc compute instance update '+module.params['machine']+' '+build_cmd_line(upd_params)+' --format=json')
                if res[0] != 0:
                    module.fail_json(msg=res[2], **result)
                result['config'] = json.loads(res[1])
                result['changed'] = True
    # if instance is found (also include after delete)
    if 'config' in result:
        # if machine must be exists, but instance is stopped
        if (module.params['state'] == 'exists') and (result['config']['status'] == 'STOPPED'):
            # Run instance if STOPPED
            if result['config']['status'] == 'STOPPED':
                res = get_oneline_param('yc compute instance start '+module.params['machine']+' --format=json')
                if res[0] != 0:
                    module.fail_json(msg=res[2], **result)
                result['config'] = json.loads(res[1])
        # Translate external IP to result
        try:
            result['ip'] = result['config']['network_interfaces'][0]['primary_v4_address']['one_to_one_nat']['address']
        except:
            pass


    # successful module execution
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
