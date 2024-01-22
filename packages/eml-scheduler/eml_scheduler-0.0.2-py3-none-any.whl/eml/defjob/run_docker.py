from clearml import Task
import os
import subprocess
from eml.utils import FileServer
from eml.utils.configs import EmlConfigs

task = Task.current_task()



EmlConfigs()._set_user(task.get_parameters()["General/username"])
eml_folder = os.path.join(EmlConfigs().eml_config["home"], ".eml/templates")

def abort_callback():
    username = EmlConfigs().eml_config["username"]
    current_worker = task.data.last_worker.replace(":", "").replace(",", "")
    exproc = subprocess.Popen('docker stop {}_{}'.format(username, current_worker), shell=True)
    exproc.wait()

task.register_abort_callback(abort_callback, 60)

fs = FileServer("")
fs.root_folder = ".eml"
ret = fs.download("templates", eml_folder)

os.chdir(eml_folder)
proc = subprocess.Popen("python template_docker.py {}".format(task.id),shell=True)
proc.wait()
