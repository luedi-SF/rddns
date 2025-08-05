# Author: luedi

import json
from fastapi import FastAPI
from pydantic import BaseModel
from requests  import get,put
from requests.exceptions import RequestException
app = FastAPI()

with open('production.json') as f:
    Config = json.load(f)
    print("readConfig:",Config)

class aItem(BaseModel):
    ip: str
    token: str

def getCFDnsDetails(domain:str,zone_id:str,email:str,api_key:str):
    try:
        with get("https://api.cloudflare.com/client/v4/zones/"+zone_id+"/dns_records",
                                  headers={
                                      "X-Auth-Email":email,
                                      "X-Auth-Key":api_key,
                                  }) as result:
            return [i for i in result.json()["result"] if i["name"]==domain][0]
    except RequestException as e:
        print(e)
        return False
def changeIP(zone_id:str,record_id:str,email:str,api_key:str,bodyjson:dict):
    try:
        with put("https://api.cloudflare.com/client/v4/zones/"+zone_id+"/dns_records/"+record_id,
                 headers={
                     "X-Auth-Email":email,
                     "X-Auth-Key":api_key,
                 },json=bodyjson) as result:
            return result.json()["result"]
    except RequestException as e:
        print(e)
        return False


@app.post("/ipnew")
async def ipnew(item: aItem):
    if item.token != Config["token"]:
        return {"code": 2}
    print("New IP change:",item.ip)
    for i in Config["domains"]:
        resp=getCFDnsDetails(i["domain"],Config["zone_id"],Config["email"],Config["api_key"])
        res=changeIP(Config["zone_id"],resp['id'],Config["email"],Config["api_key"],{
            "type": resp["type"],
            "name": resp["name"],
            "ttl": resp["ttl"],
            "content": item.ip,
            "proxied": resp["proxied"]
        })
        print("Detail:",resp)
        print("Result:", res)
        if (not res or not resp):
            return {"code": 0}


    return {"code": 1}
