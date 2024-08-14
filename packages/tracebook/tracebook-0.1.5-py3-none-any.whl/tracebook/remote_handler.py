import requests
from tracebook.config import Config

def log_push_file_to_remote_server(config: Config):
    url = config.remote_config.url
    headers = config.remote_config.headers

    with open(config.file_path, "rb") as file:
        try:
            response = requests.post(url, headers=headers, files={"file": file})
            if not response.ok:
                raise Exception(f"Failed to upload log file: {response.text}")
        except Exception as _:
            pass
