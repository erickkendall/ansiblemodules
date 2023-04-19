from ansible.module_utils.basic import AnsibleModule, missing_required_lib
import traceback
import json
PYODBC = None
try:
    import pyodbc
except ImportError:
    PYODBC_IMP_ERR = traceback.format_exc()
    MSSQL_FOUND = False
else:
    MSSQL_FOUND = True


def clean_output(o):
    return str(o)


def run_module():
    module_args = dict(

        driver=dict(default='ODBC Driver 18 for SQL Server'),
        name=dict(required=False, aliases=['db'], default=''),
        login_user=dict(),
        login_password=dict(no_log=True),
        login_host=dict(required=True),
        login_port=dict(type='int', default=1433),
        script=dict(required=True),
        output=dict(),
        params=dict(type='dict'),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    if not MSSQL_FOUND:
        module.fail_json(msg=missing_required_lib(
            'pyodbc'), exception=PYODBC_IMP_ERR)

    driver = module.params['driver']
    db = module.params['name']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    login_host = module.params['login_host']
    login_port = module.params['login_port']
    script = module.params['script']
    output = module.params['output']
    sql_params = module.params['params']


    connection_string = f"DRIVER={driver};SERVER=tcp:{login_host},{login_port};DATABASE={db};ENCRYPT=no;UID={login_user};PWD={login_password}"

    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()

            
#    # cnxn.autocommit(True)
#
#



    queries = script.split('\nGO\n')
    result['changed']=True
    if module.check_mode:
      module.exit_json(**result)

    query_results=[]
    try:
        for query in queries:
            cursor.execute(query)
            qry_result = []
            rows = cursor.fetchall()
            while rows:
              qry_result.append(rows)
              rows=cursor.fetchall()
            query_results.append(qry_result)
    except Exception as e:
      return module.fail_json(msg="query failed", query=query, error=str(e), **result)


    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()

