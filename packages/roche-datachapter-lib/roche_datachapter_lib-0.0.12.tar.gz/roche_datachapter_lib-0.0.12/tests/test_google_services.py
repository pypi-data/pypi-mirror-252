from roche_datachapter_lib.google_services import GoogleServices

GSHEET_FILE_ID = '10E9BcyglqUr14fs0nHgpNggO-x9WLBA3mronLa1a5FE'
XLS_FILE_ID = '1RWeuEPQiHgyLlD9KVSmUv3IhaNayqj6c'
SHEET_NAME = 'Sheet1'
count = 1

GS= GoogleServices()

for obj in GS.read_gsheet_data(GSHEET_FILE_ID, SHEET_NAME):
   print(obj)
   input(f"COUNT: {count}")
   count += 1
