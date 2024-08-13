import asyncio
import paramiko 
from grpclib.exceptions import GRPCError

from mergetbapi.portal.v1 import Experiment as ExperimentV1
from mergetbapi.portal.v1 import *

from .grpc_client import MergeGRPCClient, MergeGRPCError
from .identity import Identity
from .model import Model
from .realize import Realization
from .materialize import Materialization
from .xdc import XDC

"""
We make the User object a sub-class of Identity so that methods of the latter can be invoked
by objects of the former

While Merge makes a distinction between these types, most users of this library likely will not
"""
class User(Identity):
    def __init__(self, username, password=None, grpc_config=None, token=None):
        super().__init__(username, password, grpc_config, token)

    async def _async_activate(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).activate_user(
                    ActivateUserRequest(username=self.username),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_freeze(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).freeze_user(
                    FreezeUserRequest(username=self.username),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_init(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).init_user(
                    InitUserRequest(username=self.username),
                    metadata=self.get_auth_metadata()
                )
            
            return response
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).get_user(
                    GetUserRequest(
                        username=self.username,
                        status_ms=-1,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_update(self, name=None, state=None, access_mode=None,
            organizations=None, projects=None, facilities=None, experiments=None,
            toggle_admin=False):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).update_user(
                    UpdateUserRequest(
                        username=self.username,
                        name=name,
                        state=state,
                        access_mode=access_mode,
                        organizations=organizations,
                        projects=projects,
                        facilities=facilities,
                        experiments=experiments,
                        toggle_admin=toggle_admin,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_delete(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).delete_user(
                    DeleteUserRequest(user=self.username),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get_public_keys(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).get_user_public_keys(
                    GetUserPublicKeysRequest(user=self.username),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_delete_public_keys(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).delete_user_public_keys(
                    DeleteUserPublicKeysRequest(user=self.username),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_add_public_key(self, key):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).add_user_public_key(
                    AddUserPublicKeyRequest(user=self.username, key=key),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_delete_public_key(self, key):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).delete_user_public_key(
                    DeleteUserPublicKeyRequest(user=self.username, fingerprint=key),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    def activate(self):
        return asyncio.run(self._async_activate())

    def freeze(self):
        return asyncio.run(self._async_freeze())

    def init(self):
        return asyncio.run(self._async_init())

    def get(self):
        return asyncio.run(self._async_get())

    def update(self, name=None, state=None, access_mode=None, organizations=None, 
               projects=None, facilities=None, experiments=None, toggle_admin=False):
        return asyncio.run(self._async_update(
            name, state, access_mode, organizations, projects, facilities,
            experiments, toggle_admin
        ))

    def delete(self):
        return asyncio.run(self._async_delete())

    def get_public_keys(self):
        return asyncio.run(self._async_get_public_keys())  

    def delete_public_keys(self):
        return asyncio.run(self._async_delete_public_keys())

    def add_public_key(self, key):
        return asyncio.run(self._async_add_public_key(key))

    def delete_public_key(self, key):
        return asyncio.run(self._async_delete_public_key(key))

class Project(MergeGRPCClient):
    def __init__(self, name, grpc_config=None, token=None):
        super().__init__(grpc_config, token)
        self.name = name

    async def _async_create(self, username):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).create_project(
                    CreateProjectRequest(
                        user=username, # strange that the API requires this ...
                        project=self.name,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).get_project(
                    GetProjectRequest(
                        name=self.name,
                        status_ms=-1,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_update(self, description=None, access_mode=None, members=None, organization=None):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).update_project(
                    UpdateProjectRequest(
                        name=self.name,
                        description=description,
                        access_mode=access_mode,
                        members=members,
                        organization=organization,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_delete(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).delete_project(
                    DeleteProjectRequest(
                        name=self.name,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get_members(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).get_project_members(
                    GetProjectMembersRequest(
                        name=self.name,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_add_member(self, username, member):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).add_project_member(
                    AddProjectMemberRequest(
                        project=self.name,
                        username=username,
                        member=member,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get_member(self, username):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).get_project_member(
                    GetProjectMemberRequest(
                        project=self.name,
                        member=username,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_update_member(self, username, member):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).update_project_member(
                    UpdateProjectMemberRequest(
                        project=self.name,
                        username=username,
                        member=member,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_delete_member(self, username):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).delete_project_member(
                    GetProjectMemberRequest(
                        project=self.name,
                        member=username,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get_experiments(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).get_project_experiments(
                    GetProjectExperimentsRequest(
                        project=self.name,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    def create(self, username):
        return asyncio.run(self._async_create(username))

    def get(self):
        return asyncio.run(self._async_get())

    def update(self, description=None, access_mode=None, members=None, organization=None):
        return asyncio.run(self._async_update(description, access_mode, members, organization))

    def delete(self):
        return asyncio.run(self._async_delete())

    def add_member(self, username, member):
        return asyncio.run(self._async_add_member(username, member))

    def get_member(self, username):
        return asyncio.run(self._async_get_member(username))

    def update_member(self, username, member):
        return asyncio.run(self._async_update_member(username, member))

    def delete_member(self, username):
        return asyncio.run(self._async_delete_member(username))

    def get_members(self):
        return asyncio.run(self._async_get_members())

    def get_experiments(self):
        return asyncio.run(self._async_get_experiments())

class Organization(MergeGRPCClient):
    def __init__(self, name, grpc_config=None, token=None):
        super().__init__(grpc_config, token)
        self.name = name

    async def _async_create(self, username): 
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).create_organization(
                    CreateOrganizationRequest(
                        user=username, # strange that the API requires this ...
                        organization=self.name,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).get_organization(
                    GetOrganizationRequest(
                        name=self.name,
                        status_ms=-1,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_update(self, description=None, state=None, access_mode=None, members=None, projects=None):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).update_organization(
                    UpdateOrganizationRequest(
                        name=self.name,
                        description=description,
                        state=state,
                        access_mode=access_mode,
                        members=members,
                        projects=projects,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_delete(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).delete_organization(
                    DeleteOrganizationRequest(
                        name=self.name,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_activate(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).activate_organization(
                    ActivateOrganizationRequest(
                        organization=self.name,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_freeze(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).freeze_organization(
                    FreezeOrganizationRequest(
                        organization=self.name,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_request_membership(self, username, member):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).request_organization_membership(
                    RequestOrganizationMembershipRequest(
                        organization=self.name,
                        id=username,
                        kind=MembershipType.UserMember,
                        member=member,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_confirm_membership(self, username):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).confirm_organization_membership(
                    ConfirmOrganizationMembershipRequest(
                        organization=self.name,
                        id=username,
                        kind=MembershipType.UserMember,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get_member(self, username):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).get_organization_member(
                    GetOrganizationMemberRequest(
                        organization=self.name,
                        username=username,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_update_member(self, username, member):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).update_organization_member(
                    UpdateOrganizationMemberRequest(
                        organization=self.name,
                        username=username,
                        member=member,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_delete_member(self, username):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).delete_organization_member(
                    DeleteOrganizationMemberRequest(
                        organization=self.name,
                        username=username,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get_members(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).get_organization_members(
                    GetOrganizationMembersRequest(
                        organization=self.name,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get_project(self, project):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).get_organization_project(
                    GetOrganizationProjectRequest(
                        organization=self.name,
                        project=project,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get_projects(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).get_organization_projects(
                    GetOrganizationProjectsRequest(
                        organization=self.name,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    def create(self, username):
        return asyncio.run(self._async_create(username))

    def get(self):
        return asyncio.run(self._async_get())

    def update(self, description=None, state=None, access_mode=None, members=None, projects=None):
        return asyncio.run(self._async_update(
            description, state, access_mode, members, projects,
        ))

    def delete(self):
        return asyncio.run(self._async_delete())

    def activate(self):
        return asyncio.run(self._async_activate())

    def freeze(self):
        return asyncio.run(self._async_freeze())

    def request_membership(self, username, member):
        return asyncio.run(self._async_request_membership(username, member))

    def confirm_membership(self, username):
        return asyncio.run(self._async_confirm_membership(username))

    def get_member(self, username):
        return asyncio.run(self._async_get_member(username))

    def update_member(self, username, member):
        return asyncio.run(self._async_update_member(username, member))

    def delete_member(self, username):
        return asyncio.run(self._async_delete_member(username))

    def get_members(self):
        return asyncio.run(self._async_get_members())

    def get_project(self, project):
        return asyncio.run(self._async_get_project(project))

    def get_projects(self):
        return asyncio.run(self._async_get_projects())

class Experiment(MergeGRPCClient):
    def __init__(self, name, project, grpc_config=None, token=None):
        super().__init__(grpc_config, token)
        self.name = name
        self.project = project

    async def _async_create(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).create_experiment(
                    CreateExperimentRequest(
                        ExperimentV1(
                            name=self.name, 
                            project=self.project,
                        )
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get(self, with_models=None):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).get_experiment(
                    GetExperimentRequest(
                        name=self.name, 
                        project=self.project,
                        with_models=with_models,
                        status_ms=-1,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_update(self, description=None, access_mode=None, creator=None, maintainers=None):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).update_experiment(
                    UpdateExperimentRequest(
                        name=self.name, 
                        project=self.project,
                        description=description,
                        access_mode=access_mode,
                        creator=creator,
                        maintainers=maintainers,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_delete(self):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).delete_experiment(
                    DeleteExperimentRequest(
                        project=self.project,
                        experiment=self.name, 
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_get_revision(self, revision=None, encoding=None):
        try:
            async with await self.get_channel() as channel:
                return await WorkspaceStub(channel).get_revision(
                    GetRevisionRequest(
                        name=self.name, 
                        project=self.project,
                        revision=revision,
                        encoding=encoding,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    async def _async_push_model(self, modelpath, branch=None, tag=None):
        try:
            async with await self.get_channel() as channel:
                return await ModelStub(channel).push(
                    PushRequest(
                        project=self.project,
                        experiment=self.name,
                        model=Model(modelpath).contents(),
                        branch=branch,
                        tag=tag,
                    ),
                    metadata=self.get_auth_metadata()
                )
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)

    def create(self):
        return asyncio.run(self._async_create())

    def get(self, with_models=None):
        return asyncio.run(self._async_get(with_models))
        
    def update(self, description=None, access_mode=None, creator=None, maintainers=None):
        return asyncio.run(self._async_update(description, access_mode, creator, maintainers))

    def delete(self):
        return asyncio.run(self._async_delete())

    def get_revision(self, revision=None, encoding=None):
        return asyncio.run(self._async_update(revision, encoding))
 
    def push_model(self, modelpath, branch=None, tag=None):
        return asyncio.run(self._async_push_model(modelpath, branch, tag))

    def realize(self, realization, revision=None, tag=None, branch=None, duration=None):
        # call into the realize package to create an object and realize it
        return Realization(
            realization, self.name, self.project, 
            revision=revision, tag=tag, branch=branch,
            grpc_config=self.config,
        ).realize()
    
    def relinquish(self, realization):
        # call into the realize package to relinquish
        return Realization(
            realization, self.name, self.project, 
        ).relinquish()

    def materialize(self, realization):
        # call into the materialize package to create an object and materialize it
        return Materialization(
            realization, self.name, self.project, 
            grpc_config=self.config,
        ).materialize()

    def dematerialize(self, realization):
        # call into the materialize package to dematerialize
        return Materialization(
            realization, self.name, self.project, 
            grpc_config=self.config,
        ).dematerialize()

    # SPHERE trappings - alias for realize/relinquish
    def reserve(self, realization, revision=None, tag=None, branch=None, duration=None):
        return self.realize(realization, revision, tag, branch, duration)

    def free(self, realization):
        return self.relinquish(realization)

    # SPHERE trappings - alias for materialize/dematerialize
    def activate(self, realization):
        return self.materialize(realization)

    def deactivate(self, realization):
        return self.dematerialize(realization)

    def attach_xdc(self, realization, xdcname, xdcproject):
        # call into the XDC package to attach
        return XDC(
            xdcname, xdcproject,
            grpc_config=self.config,
        ).attach(realization, self.name, self.project)

    # Attach the experiment to xdc
    def detach_xdc(self, xdcname, xdcproject):
        # call into the XDC package to detach
        return XDC(
            xdcname, xdcproject,
            grpc_config=self.config,
        ).detach()
 
    # Execute command on node using SSH
    def exec_on_node(self, username, node, cmd):
        ssh_client = paramiko.SSHClient()
        private_key = paramiko.RSAKey.from_private_key_file("/home/"+username+"/.ssh/merge_key")
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(node, username=username, pkey=private_key)
        (stdin, stdout, stderr) = ssh_client.exec_command(cmd)
        lines = stdout.readlines()
        elines = stderr.readlines()
        ssh_client.close()
        return (lines, elines)
