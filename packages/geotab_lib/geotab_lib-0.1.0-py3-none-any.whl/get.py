import asyncio
import mygeotab
import datetime

async def get_data(client, typeName, resultLimit):
        res = await client.call_async('Get', typeName=typeName, resultsLimit=resultLimit)
        return res