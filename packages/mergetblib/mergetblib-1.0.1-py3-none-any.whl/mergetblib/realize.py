import asyncio
from grpclib.exceptions import GRPCError

from mergetbapi.portal.v1 import *
from .grpc_client import MergeGRPCClient, MergeGRPCError

class Realization(MergeGRPCClient):
    def __init__(self, name, experiment, project, revision=None, tag=None, branch=None,
                 duration=None, grpc_config=None, token=None):

        super().__init__(grpc_config, token)
        self.name = name
        self.experiment = experiment
        self.project = project
        self.revision = revision
        self.tag = tag
        self.branch = branch
        self.duration = duration

    async def _async_realize(self):
        try:
            async with await self.get_channel() as channel:
                return await RealizeStub(channel).realize(
                    RealizeRequest(
                        project=self.project,
                        experiment=self.experiment,
                        realization=self.name,
                        revision=self.revision,
                        tag=self.tag,
                        branch=self.branch,
                        duration=self.duration,
                    ), metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get(self):
        try:
            async with await self.get_channel() as channel:
                return await RealizeStub(channel).get_realization(
                    GetRealizationRequest(
                        project=self.project,
                        experiment=self.experiment,
                        realization=self.name,
                        status_ms=-1,
                    ), metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_update(self, duration=None):
        self.duration = duration

        try:
            async with await self.get_channel() as channel:
                return await RealizeStub(channel).update_realization(
                    UpdateRealizationRequest(
                        project=self.project,
                        experiment=self.experiment,
                        realization=self.name,
                        duration=ReservationDuration(
                            when=ReservationDurationCode.given,
                            duration=self.duration,
                        )
                    ), metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_relinquish(self):
        try:
            async with await self.get_channel() as channel:
                return await RealizeStub(channel).relinquish(
                    RelinquishRequest(
                        project=self.project,
                        experiment=self.experiment,
                        realization=self.name,
                    ), metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    def realize(self):
        return asyncio.run(self._async_realize())

    def get(self):
        return asyncio.run(self._async_get())

    def update(self, duration=None):
        return asyncio.run(self._async_update(duration))

    def relinquish(self):
        return asyncio.run(self._async_relinquish())

    # SPHERE trappings; alias for realize/relinquish
    def reserve(self):
        return self.realize()

    def free(self):
        return self.relinquish()
