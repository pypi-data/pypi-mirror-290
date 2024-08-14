from jupyter_server.base.handlers import APIHandler
import tornado
import os
import requests

# Use an environment variable for the dynamic parameter
CKAN_API_URL=os.getenv('CKAN_API_URL', '')

class DownloadRouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def post(self):
        data = self.get_json_body()
        print(data)
        result = download(data['path'], data['dataset'], data['resources'] if 'resources' in data.keys() else [])
        self.finish({"Message":f"Download Complete: {result}"})


def download(path, dataset, selected_resources=dict):
    dataset_ids = [dataset]

    is_success = True

    for dataset_id in dataset_ids:
        folder_path = f'./{path}/' + dataset_id

        # Ensure the folder exists
        os.makedirs(folder_path, exist_ok=True)

        # get all resources in package from CKAN API
        endpoint = 'package_show'
        ckan_resources = requests.get(CKAN_API_URL + endpoint, params={"id": dataset_id}, verify=False).json()['result']['resources']
        ckan_resources = {x['name']: x['url'] for x in ckan_resources}
        print(f"CKAN Resources: {ckan_resources}")

        # if not passed, download all resources using CKAN links
        if not selected_resources:
            resources_to_download = ckan_resources
        # if passed, replace passed by urls from ckan_resources (because Workspaces api might give false urls)
        else:
            print(f"Selected Resources: {selected_resources}")
            # make intersection of 2 dicts, leaving values of CKAN dict
            resources_to_download = {resource_name: ckan_resources[resource_name] for resource_name in ckan_resources if resource_name in selected_resources}

        # download resources one by one
        print(f"Resources to Download: {resources_to_download}")
        for resource_name, resource_url in resources_to_download.items():
            url = resource_url
            print(f'Trying URL:', url)
            if not url:
                print("Not URL")
                continue
            try:
                response = requests.get(url, verify=False)
                print(f'Got response {response.status_code}')

                # Check if the request was successful
                if response.status_code == 200:
                    # Extracting the filename from the URL
                    filename = url.split('/')[-1]
                    file_path = os.path.join(folder_path, filename)

                    # Saving the file
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"{filename} downloaded successfully.")
                else:
                    is_success = False
                    print(f"Failed to download {url}")

            except requests.exceptions.MissingSchema:
                is_success = False
                print(f'Unknown URL: {url}')
    return is_success