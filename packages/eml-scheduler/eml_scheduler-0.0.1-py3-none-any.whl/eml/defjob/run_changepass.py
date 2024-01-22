from clearml import Task
import os
from eml.utils import FileServer
from eml.utils.configs import EmlConfigs

task = Task.current_task()

EmlConfigs()._set_user(task.get_parameters()["General/username"])
eml_folder = os.path.join(EmlConfigs().eml_config["home"], ".eml/templates")

fs = FileServer("")
fs.root_folder = ".eml"
ret = fs.download("templates", eml_folder)

os.chdir(eml_folder)
os.system("python change_pass.py {}".format(task.id))
