from jupyter_server.utils import url_path_join
from ndp_jupyterlab_extension.download_datasets import DownloadRouteHandler
from ndp_jupyterlab_extension.get_workspaces_data import GetWorkspacesDataRouteHandler
from ndp_jupyterlab_extension.install_requirements import InstallRequirementsRouteHandler


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern_download = url_path_join(base_url, "ndp-jupyterlab-extension", "download_datasets")
    route_pattern_install = url_path_join(base_url, "ndp-jupyterlab-extension", "install_requirements")
    route_pattern_get_workspaces_data = url_path_join(base_url, "ndp-jupyterlab-extension", "get_workspaces_data")
    handlers = [
        (route_pattern_download, DownloadRouteHandler),
        (route_pattern_install, InstallRequirementsRouteHandler),
        (route_pattern_get_workspaces_data, GetWorkspacesDataRouteHandler),
    ]
    web_app.add_handlers(host_pattern, handlers)
