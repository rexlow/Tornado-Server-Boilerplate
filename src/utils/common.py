#!/usr/bin/python3

import urllib
from .DotDict import DotDict

def parseEncodedString(encodedString: str):
    return urllib.parse.unquote(urllib.parse.unquote(encodedString))

def formatRequestBody(data) -> dict:
    dataDict = { parseEncodedString(k):parseEncodedString(v) for k,v in (x.split('=') for x in data) }
    dataDict = DotDict(dataDict)
    return dataDict

def unloadRequestParams(data):
    res = {}
    for k, v in data.items():
        res[k] = data[k][0].decode(encoding="utf-8")
    return res