from sys import path
from roche_datachapter_lib.db_config import DB_CONFIG
print(path)
#DB_CONFIG.execute_custom_select_query("SELECT 1+1 as res", 'sqlserver_master')