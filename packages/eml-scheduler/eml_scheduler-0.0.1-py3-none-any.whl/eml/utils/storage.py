import os
import json
from tqdm import tqdm
from clearml import StorageManager
from .checksum import get_checksum_file
from .configs import EmlConfigs
import pathspec


class FileServer:
    def __init__(self, taskname):
        self.remote_path = StorageManager.get_files_server()
        self.configs = EmlConfigs()
        self.root_folder = os.path.join(
            self.configs.clearml_config["username"], taskname
        )

    def generate_checksum_file(self, path, files_path):
        checksum_file = os.path.join(path, self.configs.CHECKSUM_FILE_NAME)
        checksum_dict = {}
        for file in files_path:
            checksum = get_checksum_file(os.path.join(path, file))
            checksum_dict[file] = checksum

        with open(checksum_file, "w") as f:
            json.dump(checksum_dict, f)

        return checksum_dict

    def get_checksums(self, path):
        _, folder_name = os.path.split(path)
        remote_path = os.path.join(
            self.remote_path,
            self.root_folder,
            folder_name,
            self.configs.CHECKSUM_FILE_NAME,
        )
        local_cache = os.path.join(path, self.configs.CACHE_FOLDER_NAME)
        local_cache_project = os.path.join(local_cache, self.root_folder, folder_name)
        os.makedirs(local_cache_project, exist_ok=True)
        local_path = os.path.join(local_cache_project, self.configs.CHECKSUM_FILE_NAME)
        with open(local_path, "w") as f:
            json.dump({}, f)
        try:
            StorageManager.download_file(
                remote_url=remote_path,
                local_folder=local_cache,
                overwrite=True,
            )
        except:
            pass

        with open(local_path, "r") as f:
            server_checksums = json.load(f)

        os.remove(local_path)
        return server_checksums

    def upload_file(self, path, file_path, wait_for_upload=True):
        local_path = os.path.join(path, file_path)
        _, folder_name = os.path.split(path)
        remote_path = os.path.join(
            self.remote_path, self.root_folder, folder_name, file_path
        )
        StorageManager.upload_file(
            local_file=local_path,
            remote_url=remote_path,
            wait_for_upload=wait_for_upload,
        )
        return StorageManager.exists_file(remote_path)

    def list_files(self, folder_path):
        files_path = []
        init_path = len(folder_path)
        for path, _, files in os.walk(folder_path):
            for file_name in files:
                relative_path = os.path.join(path[init_path:], file_name)
                if relative_path[0] == "/":
                    relative_path = relative_path[1:]
                files_path.append(relative_path)

        return files_path

    def filter_files(self, files_path, folder_path):
        exclusion_file = os.path.join(folder_path, self.configs.EXCLUSION_FILE_NAME)
        if not os.path.exists(exclusion_file):
            exclusion_file = exclusion_file.replace("emlignore", ".gitignore")
        if not os.path.exists(exclusion_file):
            return [f for f in files_path if self.configs.CACHE_FOLDER_NAME not in f]
        with open(exclusion_file, "r") as f:
            spec = pathspec.PathSpec.from_lines(
                "gitwildmatch",
                f,
            )
        for excluded in spec.match_files(files_path):
            files_path.remove(excluded)
        return [f for f in files_path if self.configs.CACHE_FOLDER_NAME not in f]

    def upload_folder(self, path):
        files_path = self.list_files(path)
        files_path = self.filter_files(files_path, path)
        checksums = self.generate_checksum_file(path, files_path)
        files_path.append(self.configs.CHECKSUM_FILE_NAME)
        server_checksums = self.get_checksums(path)
        print(
            "Uploading files to {}/{}".format(
                self.configs.clearml_config["username"], os.path.split(path)[1]
            )
        )
        num_files = len(files_path) - 1
        for file_index, file in tqdm(enumerate(files_path)):
            if (file not in server_checksums) or (
                server_checksums[file] != checksums[file]
            ):
                if not self.upload_file(path, file, True):
                    print("Error uploading file {}".format(file))
                    return False
        return True

    def download(self, remote_folder, local_folder, overwrite=False):
        remote_path = os.path.join(self.remote_path, self.root_folder, remote_folder)
        temp_local_folder = os.path.join(local_folder, self.configs.CACHE_FOLDER_NAME)
        os.makedirs(temp_local_folder, exist_ok=True)
        StorageManager.download_file(
            os.path.join(remote_path, self.configs.CHECKSUM_FILE_NAME),
            temp_local_folder,
            overwrite=True,
        )
        temp_local_folder_project = os.path.join(
            temp_local_folder, self.root_folder, remote_folder
        )
        checksum_file = os.path.join(
            temp_local_folder_project, self.configs.CHECKSUM_FILE_NAME
        )
        if os.path.exists(checksum_file):
            with open(checksum_file, "r") as f:
                checksums = json.load(f)
        else:
            checksums = {}

        for file, temp_checksum in tqdm(checksums.items()):
            temp_file = os.path.join(temp_local_folder_project, file)
            local_file = os.path.join(local_folder, file)
            DOWNLOAD_FLAG = False
            REMOVE_LOCAL_FLAG = False
            if os.path.exists(local_file):
                REMOVE_LOCAL_FLAG = True
                local_checksum = get_checksum_file(local_file)
                if (local_checksum != temp_checksum) or overwrite:
                    DOWNLOAD_FLAG = True
            else:
                DOWNLOAD_FLAG = True
            if DOWNLOAD_FLAG:
                StorageManager.download_file(
                    os.path.join(remote_path, file),
                    temp_local_folder,
                    overwrite=True,
                )
                if os.path.exists(temp_file):
                    folder, _ = os.path.split(local_file)
                    os.makedirs(folder, exist_ok=True)
                    if REMOVE_LOCAL_FLAG:
                        os.remove(local_file)
                    os.rename(temp_file, local_file)

        return checksums
