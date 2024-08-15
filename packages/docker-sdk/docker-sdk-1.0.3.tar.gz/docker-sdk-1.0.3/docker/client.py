
import asyncio
import aiohttp
from containers import Containers 
from networks import Networks 
from volumes import Volumes 
from system import System
from  session import Session
from exec import Exec
from images import Images

class Client:
    def __init__(self,hostname,port):
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1000))
        self.containers = Containers(hostname = hostname,port = port,session = self.session)
        self.networks = Networks(hostname = hostname,port = port,session = self.session)
        self.volumes = Volumes(hostname = hostname,port = port,session = self.session)
        self.system = System(hostname = hostname,port = port,session = self.session)
        self.exec = Exec(hostname = hostname,port = port,session = self.session)
        self.images = Images(hostname = hostname,port = port,session = self.session)
        
        
        
    async def close(self):
        """
        Close ClientSession.
        """
        await self.session.close()
        