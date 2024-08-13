from .utils import *
from .abstract_call import *
from abstract_apis import *
def getFlaskRequest(endpoint,**kwargs):
  return getPostRequest(getFlaskUrl(),kwargs,endpoint=endpoint)

def view_table(table_name, column_name=None, start=None, end=None, filters=None, search_string=None,deep_search=False,latest=None,**kwargs):
  return getFlaskRequest('view_table',table_name=table_name,column_name=column_name, start=start, end=end, filters=filters, search_string=search_string,deep_search=deep_search,latest=latest,**kwargs)

def getLpKeys(table_name=None, column_name=None, start=None, end=None, filters=None, search_string=None,deep_search=False,latest=None,**kwargs):
  response = view_table(table_name=table_name or 'key_info',column_name=column_name, start=start, end=end, filters=filters, search_string=search_string,deep_search=deep_search,latest=latest,**kwargs)
  signature=response[0].get('signature')
  return getCallRequest('getLpKeys',signature)

def list_tables(with_data=True):
  response = getGetRequest(getFlaskUrl(), data={"with_data":with_data},endpoint='list_tables')
  return response

def list_columns(table_name=None):
  tables = {}
  table_names = make_list(table_name or list_tables(with_data=True))
  for tableName in table_names:
    tables[tableName]= getGetRequest(getFlaskUrl(), data={"table_name":tableName},endpoint="list_columns")
  return tables
