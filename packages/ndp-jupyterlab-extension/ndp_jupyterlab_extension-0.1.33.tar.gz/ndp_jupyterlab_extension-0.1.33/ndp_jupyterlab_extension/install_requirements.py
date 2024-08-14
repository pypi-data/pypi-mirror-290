import subprocess
import json
from jupyter_server.base.handlers import APIHandler
import tornado
import os

class InstallRequirementsRouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def post(self):
        data = self.get_json_body()
        print(data)
        install_requirements(data['path'])
        self.finish(json.dumps({"message": "requirements installed"}))

def install_requirements(path):
    # install requirements.txt packages

    # Construct the full file path for requirements.txt
    requirements_path = os.path.join(path, 'requirements.txt')

    # Check if requirements.txt exists
    if os.path.isfile(requirements_path):
        print(f"Found requirements.txt at {requirements_path}. Installing libraries...")
        # Run pip install command
        result = subprocess.run(['pip', 'install', '-r', requirements_path], capture_output=True, text=True)
        if result.returncode == 0:
            print("Libraries installed successfully.")
        else:
            print("An error occurred while installing libraries.")
            print(result.stdout)
            print(result.stderr)
    else:
        print("No requirements.txt found in the directory.")
