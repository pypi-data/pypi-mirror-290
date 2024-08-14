import json
from jupyter_server.base.handlers import APIHandler
import tornado
import os
import requests

# Use an environment variable for the dynamic parameter
WORKSPACE_API_URL=os.getenv('WORKSPACE_API_URL', '')

class GetWorkspacesDataRouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        access_token = os.getenv('ACCESS_TOKEN', '')
        if not access_token:
            from ndp_jupyterlab_extension import get_tokens
            get_tokens()

        # Get data
        endpoint_url = f"{WORKSPACE_API_URL}/workspace/read_workspaces_by_user"

        payload = {}
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        print(f'Using Access Token: {access_token}')
        response = requests.request("GET", endpoint_url, headers=headers, data=payload, verify=False)
        print(json.dumps(response.json(), indent=4))
        self.finish(json.dumps(response.json()))

