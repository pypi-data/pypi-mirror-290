import asyncio
from grpclib.exceptions import GRPCError

from mergetbapi.portal.v1 import *
from .grpc_client import MergeGRPCClient, MergeGRPCError

class Identity(MergeGRPCClient):
    def __init__(self, username, password=None, grpc_config=None, token=None):
        super().__init__(grpc_config, token)
        self.username = username
        self.password = password

    async def _async_login(self):
        try:
            async with await self.get_channel() as channel:
                response = await IdentityStub(channel).login(
                    LoginRequest(username=self.username, password=self.password)
                )

            self.set_bearer_token(response.token)
            return response
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_logout(self):
        try:
            async with await self.get_channel() as channel:
                return await IdentityStub(channel).logout(
                    LogoutRequest(username=self.username), 
                    metadata=self.get_auth_metadata(),
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get(self):
        try:
            async with await self.get_channel() as channel:
                return await IdentityStub(channel).get_identity(
                    GetIdentityRequest(username=self.username),
                    metadata=self.get_auth_metadata(),
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_register(self, password, email, institution, category, country, usstate, name, admin=False):
        try:
            async with await self.get_channel() as channel:
                return await IdentityStub(channel).register(RegisterRequest(
                    username=self.username,
                    email=email,
                    password=password,
                    institution=institution,
                    category=category,
                    country=country,
                    usstate=usstate,
                    name=name,
                    admin=admin
                ))
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_unregister(self):
        try:
            async with await self.get_channel() as channel:
                return IdentityStub(channel).register(UnregisterRequest(
                    username=self.username,
                    metadata=self.get_auth_metadata(),
                ))
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    def login(self):
        return asyncio.run(self._async_login())

    def logout(self):
        return asyncio.run(self._async_logout())

    def get(self):
        return asyncio.run(self._async_get())
        
    def register(self, password, email, institution, category, country, usstate, name, admin=False):
        return asyncio.run(self._async_register(
            email, institution, category, country, usstate, name, admin
        ))

    def unregister(self):
        return asyncio.run(self._async_unregister())
