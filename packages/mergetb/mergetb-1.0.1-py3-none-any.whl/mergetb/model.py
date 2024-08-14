import asyncio
import tempfile
import validators
from urllib.request import urlretrieve
from grpclib.exceptions import GRPCError

from mergetbapi.portal.v1 import *

from .grpc_client import MergeGRPCClient, MergeGRPCError

class Model(MergeGRPCClient):
    def __init__(self, modelpath, grpc_config=None):
        super().__init__(grpc_config),
        self.model = modelpath

    async def _async_compile(self):
        try:
            async with await self.get_channel() as channel:
                return await ModelStub(channel).compile(
                    CompileRequest(model=self.contents()),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)
 
    def contents(self):
        if validators.url(self.model):
            with tempfile.NamedTemporaryFile() as tmp:
                urlretrieve(self.model, tmp.name)
                return open(tmp.name, 'r').read()
        else:
            return open(self.model, 'r').read()

    def compile(self):
        return asyncio.run(self._async_compile())
