import datetime

try:
    from ._version import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip. It is highly recommended to install
    # the package from a stable release or in editable mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    import warnings
    warnings.warn("Importing 'ndp_jupyterlab_extension' outside a proper installation.")
    __version__ = "dev"
from .handlers import setup_handlers
from keycloak import KeycloakOpenID
import os

KEYCLOAK_URL=os.getenv('KEYCLOAK_URL', '')
KEYCLOAK_CLIENT_ID=os.getenv('KEYCLOAK_CLIENT_ID', '')
KEYCLOAK_CLIENT_SECRET=os.getenv('KEYCLOAK_CLIENT_SECRET', '')
KEYCLOAK_REALM=os.getenv('KEYCLOAK_REALM', '')

def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "ndp-jupyterlab-extension"
    }]


def _jupyter_server_extension_points():
    return [{
        "module": "ndp_jupyterlab_extension"
    }]


def _load_jupyter_server_extension(server_app):
    """Registers the API handler to receive HTTP requests from the frontend extension.

    Parameters
    ----------
    server_app: jupyterlab.labapp.LabApp
        JupyterLab application instance
    """
    setup_handlers(server_app.web_app)
    name = "ndp_jupyterlab_extension"
    server_app.log.info(f"Registered {name} server extension")


def get_tokens():
    keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                     client_id=KEYCLOAK_CLIENT_ID,
                                     realm_name=KEYCLOAK_REALM,
                                     client_secret_key=KEYCLOAK_CLIENT_SECRET)

    try:
        tokens = keycloak_openid.refresh_token(os.environ['REFRESH_TOKEN'])
        print("Refreshing token")
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        os.environ['REFRESH_TOKEN'] = refresh_token
        os.environ['ACCESS_TOKEN'] = access_token
        os.environ['TOKEN_ATTEMPT_TIME_AUTO'] = str(datetime.datetime.now())
        print("Refreshed token")
        return access_token
    except:
        print("Error while refreshing token")

import threading
import time

def background_task():
    while True:
        # Your function logic here
        get_tokens()
        print("Waiting 3 minutes")
        time.sleep(180)  # Run every 3 minutes

# Start the background thread
background_thread = threading.Thread(target=background_task, daemon=True)
background_thread.start()


