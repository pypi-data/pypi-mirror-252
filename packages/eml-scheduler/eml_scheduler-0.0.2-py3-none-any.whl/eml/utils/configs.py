import os
from clearml.backend_config.config import Config
from clearml import StorageManager


class ClearmlConfigs:
    def __init__(self, path="~/eml.conf"):
        self.path = os.path.expanduser(path)
        self._config = {}
        if os.path.exists(self.path):
            try:
                clearml_config = Config(verbose=False)._read_single_file(
                    file_path=self.path, verbose=False
                )
                self._config["access_key"] = clearml_config["api"]["credentials"][
                    "access_key"
                ]
                self._config["username"] = clearml_config["eml"]["username"]

            except:
                pass

    def __getitem__(self, key):
        try:
            return self._config[key]
        except:
            raise Exception("No {} found in {}".format(key, self.path))


class EmlConfigs:
    def __new__(self):
        self._newist = False
        if not hasattr(self, "_instance"):
            self._instance = super(EmlConfigs, self).__new__(self)
            self._newist = True
        return self._instance

    def __init__(self):
        if self._newist:
            self.CLEARML_FILE_NAME = "~/eml.conf"
            self.EML_FOLDER_NAME = "eml"
            self.EXCLUSION_FILE_NAME = os.path.join("emlignore")
            self.CHECKSUM_FILE_NAME = os.path.join("checksum.json")
            self.CACHE_FOLDER_NAME = os.path.join(".emlcache")
            self.clearml_config = ClearmlConfigs(self.CLEARML_FILE_NAME)
            self.EML_FILE_NAME = os.path.expanduser(
                "~/.eml/configs/{}.conf".format(self.clearml_config["username"])
            )

            StorageManager.download_file(
                os.path.join(
                    StorageManager.get_files_server(),
                    ".eml/configs",
                    "{}.conf".format(self.clearml_config["username"]),
                ),
                os.path.expanduser("~"),
                overwrite=True,
            )

            self.eml_config = {}
            if os.path.exists(self.EML_FILE_NAME):
                self.eml_config = Config()._read_single_file(
                    file_path=self.EML_FILE_NAME, verbose=False
                )["config"]

    def _set_user(self, user):
        StorageManager.download_file(
            os.path.join(
                StorageManager.get_files_server(),
                ".eml/configs",
                "{}.conf".format(user),
            ),
            os.path.expanduser("~"),
            overwrite=True,
        )
        self.EML_FILE_NAME = os.path.expanduser("~/.eml/configs/{}.conf".format(user))
        self.eml_config = Config(verbose=False)._read_single_file(
            file_path=self.EML_FILE_NAME, verbose=False
        )["config"]
