from abstract_solcatcher.utils import *
from abstract_apis import *

def asyncCallRequest(endpoint,*args,**kwargs):
  endpoint = make_endpoint(endpoint)
  return postRequest(getCallUrl(),kwargs,endpoint=endpoint)

def getCallArgs(endpoint):
  return {'getMetaData': ['signature'], 'getPoolData': ['signature'], 'getTransactionData': ['signature'], 'getPoolInfo': ['signature'], 'getMarketInfo': ['signature'], 'getKeyInfo': ['signature'], 'getLpKeys': ['signature'], 'process': ['signature']}.get(get_endpoint(endpoint))
endpoint = 'getTransaction'
signature = "5F64gV7VhHJPnwJF4tEDzUCSErz7weC37HiArnLbu3xRDBFrSWcJPKZ2LNJYpuyK42KRKo373JnEiF3CdwHP8DFo"

input(f"{getCallUrl()}/{endpoint}")
input(requests.get(f"{getCallUrl()}/{endpoint}",{"signature":signature}))
