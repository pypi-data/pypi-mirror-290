import asyncio
from grpclib.exceptions import GRPCError

from mergetbapi.portal.v1 import *

from .grpc_client import MergeGRPCClient, MergeGRPCError

class XDC(MergeGRPCClient):
    def __init__(self, name, project, xdctype=XdcType.personal, grpc_config=None, token=None):
        super().__init__(grpc_config, token)
        self.name = name
        self.project = project
        self.xdctype = xdctype

    async def _async_create(self):
        try:
            async with await self.get_channel() as channel:
                return await XdcStub(channel).create_xdc(
                    CreateXdcRequest(
                        project=self.project,
                        xdc=self.name,
                        type=self.xdctype,
                    ), metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get(self):
        try:
            async with await self.get_channel() as channel:
                return await XdcStub(channel).get_xdc(
                    GetXdcRequest(
                        project=self.project,
                        xdc=self.name,
                        status_ms=-1,
                    ), metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_delete(self):
        try:
            async with await self.get_channel() as channel:
                return await XdcStub(channel).delete_xdc(
                    DeleteXdcRequest(
                        project=self.project,
                        xdc=self.name,
                    ), metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_attach(self, realization, experiment, project):
        try:
            async with await self.get_channel() as channel:
                return await XdcStub(channel).attach_xdc(
                    AttachXdcRequest(
                        xdc=self.name,
                        project=self.project,
                        experiment=experiment,
                        realization=realization,
                        realization_project=project,
                    ), metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_detach(self):
        try:
            async with await self.get_channel() as channel:
                return await XdcStub(channel).detach_xdc(
                    DetachXdcRequest(
                        xdc=self.name,
                        project=self.project,
                    ), metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_detach(self):
        try:
            async with await self.get_channel() as channel:
                return await XdcStub(channel).detach_xdc(
                    DetachXdcRequest(
                        xdc=self.name,
                        project=self.project,
                    ), metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    def create(self):
        return asyncio.run(self._async_create())

    def get(self):
        return asyncio.run(self._async_get())

    def delete(self):
        return asyncio.run(self._async_delete())

    def attach(self, realization, experiment, project):
        return asyncio.run(self._async_attach(realization, experiment, project))

    def detach(self):
        return asyncio.run(self._async_detach())
