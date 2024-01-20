from aiohttp import ClientSession
import ujson

class Requests:
    session = None
    def __init__(self) -> None:
        pass

    async def sendRequest(self, data, method):
        session = ClientSession(headers={'Content-Type': 'application/json'}, json_serialize=ujson.dumps)
        async with session as s:
            async with s.post("https://api.keksik.io/"+method,
                                    json=data) as conn:
                responce = ujson.loads((await conn.content.read()).decode())
                if responce['success']:
                    return responce
                else:
                    raise Exception(responce['error'], responce['msg'])


class KeksikApi:
    def __init__(self,
                group_id=None,
                token=None,
                v=1):
        self.group_id = abs(group_id)
        self.token = str(token)
        self.v = v
        self.sendRequest = Requests().sendRequest
        self.donates = self.donates(self.sendRequest, self.group_id, self.token, self.v)
        self.campaigns = self.campaigns(self.sendRequest, self.group_id, self.token, self.v)
        self.payments = self.payments(self.sendRequest, self.group_id, self.token, self.v)

    class donates:
        def __init__(self,
                     sendRequest,
                group_id=None,
                token=None,
                v=1):
            self.group_id = abs(group_id)
            self.token = str(token)
            self.v = v
            self.sendRequest = sendRequest
        
        async def get(self,
            length=20,
            offset=None,
            start_date=None,
            end_date=None,
            sort=None,
            reverse=None
            ) -> list:
            post_args = {
                'group':self.group_id,
                'token':self.token,
                'v':self.v,
                'len':length,
                'offset':offset,
                'start_date':start_date,
                'end_date':end_date,
                'sort':sort,
                'reverse':reverse
                }
            return (await self.sendRequest(post_args, 'donates/get'))['list']
        
        async def getLast(self, last=None) -> list:
            post_args = {
                'group':self.group_id,
                'token':self.token,
                'v':self.v,
                'last':last
                }
            return (await self.sendRequest(post_args, 'donates/get-last'))['list']
        
        async def changeStatus(self, id, status) -> bool:
            post_args = {
                'group':self.group_id,
                'token':self.token,
                'v':self.v,
                'id':id,
                'status':status
                }

            return (await self.sendRequest(post_args, 'donates/change-status'))['success']
        
        async def answer(self, id, answer) -> bool:
            post_args = {
                'group':self.group_id,
                'token':self.token,
                'v':self.v,
                'id':id,
                'answer':answer
                }

            return (await self.sendRequest(post_args, 'donates/answer'))['success']
        
        async def changeRewardStatus(self, id, status) -> bool:
            post_args = {
                'group':self.group_id,
                'token':self.token,
                'v':self.v,
                'id':id,
                'status':status
                }

            return (await self.sendRequest(post_args, 'donates/change-reward-status'))['success']

    class campaigns:
        def __init__(self,
                     sendRequest,
                group_id=None,
                token=None,
                v=1):
            self.group_id = abs(group_id)
            self.token = str(token)
            self.v = v
            self.sendRequest = sendRequest
        
        async def get(self, ids=None) -> list:
            post_args = {
                'group':self.group_id,
                'token':self.token,
                'v':self.v,
                'ids':ids
                }

            return (await self.sendRequest(post_args, 'campaigns/get'))['list']
        
        async def getActive(self) -> dict:
            post_args = {
                'group':self.group_id,
                'token':self.token,
                'v':self.v
                }

            return (await self.sendRequest(post_args, 'campaigns/get-active'))['campaign']
        
        async def getRewards(self, campaign) -> list:
            post_args = {
                'group':self.group_id,
                'token':self.token,
                'v':self.v,
                'campaign':campaign
                }

            return (await self.sendRequest(post_args, 'campaigns/get-rewards'))['list']
        
        async def change(self,
            id,
            title=None,
            status=None,
            end=None,
            point=None,
            start_received=None,
            start_backers=None
            ) -> bool:
            post_args = {
                'group':self.group_id,
                'token':self.token,
                'v':self.v,
                'id':id,
                'title':title,
                'status':status,
                'end':end,
                'point':point,
                'start_received':start_received,
                'start_backers':start_backers
                }

            return (await self.sendRequest(post_args, 'campaigns/change'))['success']
        
        async def changeReward(self,
            id,
            title=None,
            desc=None,
            min_donate=None,
            limits=None,
            status=None
            ) -> bool:
            post_args = {
                'group':self.group_id,
                'token':self.token,
                'v':self.v,
                'id':id,
                'title':title,
                'desc':desc,
                'min_donate':min_donate,
                'limits':limits,
                'status':status
                }

            return (await self.sendRequest(post_args, 'campaigns/change-reward'))['success']

    class payments:
        def __init__(self,
                     sendRequest,
                group_id=None,
                token=None,
                v=1):
            self.group_id = abs(group_id)
            self.token = str(token)
            self.v = v
            self.sendRequest = sendRequest
            
        
        async def get(self, ids=None) -> list:
            post_args = {
                'group':self.group_id,
                'token':self.token,
                'v':self.v,
                'ids':ids
                }

            return (await self.sendRequest(post_args, 'payments/get'))['list']
        
        async def create(self, 
            system,
            purse,
            amount,
            name=None
            ) -> int:
            post_args = {
                'group':self.group_id,
                'token':self.token,
                'v':self.v,
                'system':system,
                'purse':purse,
                'name':name,
                'amount':amount
                }

            return (await self.sendRequest(post_args, 'payments/create'))['int']
    
    async def balance(self) -> int:
        post_args = {
            'group':self.group_id,
            'token':self.token,
            'v':self.v,
            }

        return (await self.sendRequest(post_args, 'balance'))['balance']

