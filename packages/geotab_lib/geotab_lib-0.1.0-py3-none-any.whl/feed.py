import asyncio
import mygeotab
import datetime

async def get_feed(client, typeName, resultLimit, fromDate=None, fromVersion=None):
    if(fromVersion != None):
        res = await client.call_async('GetFeed', typeName=typeName, resultsLimit=resultLimit, fromVersion=fromVersion, search={
                'fromDate': fromDate if fromDate != None else datetime.datetime.now().isoformat()
        })

        return res
    else:
        res = await client.call_async('GetFeed', typeName=typeName, resultsLimit=resultLimit, search={
            'fromDate': fromDate if fromDate != None else datetime.datetime.now().isoformat()
        })

        return res