def getSolcatcherUrl():
  return 'https://solcatcher.io'
def getFlaskEndpoint():
  return 'getDbData'
def getCallEndpoint():
  return 'getSolData'
def getRateLimitEndpoint():
  return 'rateLimiter'
def getFlaskUrl():
  return f"{getSolcatcherUrl()}/{getFlaskEndpoint()}"
def getCallUrl():
  return f"{getSolcatcherUrl()}/{getCallEndpoint()}"
def getRateLimitUrl():
  return f"{getSolcatcherUrl()}/{getRateLimitEndpoint()}"
def updateData(data,**kwargs):
  data.update(kwargs)
  return data
