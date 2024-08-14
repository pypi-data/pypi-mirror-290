import asyncio
from grpclib.exceptions import GRPCError

from mergetbapi.portal.v1 import *

from .grpc_client import MergeGRPCClient, MergeGRPCError

class Materialization(MergeGRPCClient):
    def __init__(self, name, experiment, project, grpc_config=None, token=None):
        super().__init__(grpc_config, token)
        self.name = name
        self.experiment = experiment
        self.project = project

    async def _async_materialize(self):
        try:
            async with await self.get_channel() as channel:
                return await MaterializeStub(channel).materialize(
                    MaterializeRequest(
                        project=self.project,
                        experiment=self.experiment,
                        realization=self.name,
                    ), metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get(self):
        try:
            async with await self.get_channel() as channel:
                return await MaterializeStub(channel).get_materialization_v2(
                    GetMaterializationRequestV2(
                        project=self.project,
                        experiment=self.experiment,
                        realization=self.name,
                        status_ms=-1,
                    ), metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_dematerialize(self):
        self.duration = duration

        try:
            async with await self.get_channel() as channel:
                return await MaterializeStub(channel).dematerialize(
                    DematerializeRequest(
                        project=self.project,
                        experiment=self.experiment,
                        realization=self.name,
                    ), metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    def materialize(self):
        return asyncio.run(self._async_materialize())

    def get(self):
        return asyncio.run(self._async_get())

    def dematerialize(self):
        return asyncio.run(self._async_dematerialize())

    # SPHERE trappings - alias for materialize/dematerialize
    def activate(self):
        return self.materialize()

    def deactivate(self):
        return self.dematerialize()
