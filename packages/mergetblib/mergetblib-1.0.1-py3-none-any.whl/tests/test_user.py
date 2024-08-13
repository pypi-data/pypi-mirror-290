import sys

# mergetblib imports
import mergetblib.mergetb as mergetb
from mergetblib.workspace import User
from mergetblib.types import StatusType
from mergetblib.grpc_client import MergeGRPCError

# common test package imports
from .test_common import check_prompt_credentials

try:
    # Login to your account via the User object 
    username, password = check_prompt_credentials()

    user = User(username, password)
    token = user.login().token
    print("Logged in for user %s" % username)

    resp = user.get().user
    summary="""User info for %s:
    Name:          %s
    State:         %s
    Access Mode:   %s
    Uid:           %d
    Gid:           %d
    Projects:      %s
    Experiments:   %s
    Organizations: %s
    Facilities:    %s
    Admin:         %d
    Institution:   %s
    Category:      %s
    Email:         %s
    Country:       %s
    US State:      %s""" % (
        username,
        resp.name,
        resp.state,
        resp.access_mode,
        resp.uid,
        resp.gid,
        resp.projects,
        resp.experiments,
        resp.organizations,
        resp.facilities,
        resp.admin,
        resp.institution,
        resp.category,
        resp.email,
        resp.country,
        resp.usstate,
    )
    print(summary)

    projects = mergetb.get_projects().projects
    
    print()
    print("User has the following projects:")
    for project in projects:
        summary="""Project: %s
    Description:  %s
    Members:      %s
    Experiments:  %s
    Access Mode:  %d
    GID:          %d
    Organization: %s
    Category:     %s
    Subcategory:  %s""" % (
            project.name,
            project.description,
            project.members,
            project.experiments,
            project.access_mode,
            project.gid,
            project.organization,
            project.category,
            project.subcategory,
        )
        print(summary)

# API errors are raised as MergeGRPCError
except MergeGRPCError as e:
    print(e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
else:
    print("test PASSED")
    sys.exit(0)

print("test FAILED")
sys.exit(1)
