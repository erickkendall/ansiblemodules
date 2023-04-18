#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: ans

short_descripton: This is my test module

'''

def run_module():

    module_args = dict(
            name=dict(type='str', required=True),
            new=dict(type='bool', required=False, default=False)
    )

    result=dict(
            changed=False,
            original_message='',
            message=''

    )

    module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)


    result['original_message']=module.params['name']
    result['changed']=True

    if module.params['new']:
        result['changed']=True

    if module.params['name']=='fail me':
        resulte['changed']=True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
