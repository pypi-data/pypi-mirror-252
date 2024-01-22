import argparse
from tqdm import tqdm
from clearml import Task
from prettytable import PrettyTable

from eml.utils.configs import EmlConfigs


def get_task(tid):
    config = EmlConfigs()
    task = Task.get_task(task_id=tid)
    if task and task.data.user == config.eml_config["id"]:
        return task

    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--id",
        help="Task ID",
        required=True,
    )
    args = parser.parse_args()

    t = get_task(args.id)
    if not t:
        print("Task not found")
        return

    tab = PrettyTable(["Fields", "Value"])
    params = {k.replace("General/", ""): v for k, v in t.get_parameters().items()}
    project_name = t.get_project_name().split("/")
    if len(project_name) > 1:
        project_name = "/".join(project_name[1:])
    tab.add_row(["ID", t.id])
    tab.add_row(["Project", project_name])
    tab.add_row(["Status", t.status])
    tab.add_row(["Created", t.data.created.strftime("%d/%m/%Y, %H:%M:%S")])
    tab.add_row(["Last Update", t.data.last_update.strftime("%d/%m/%Y, %H:%M:%S")])
    tab.add_row(
        ["Script", params.get("working_dir", "") + "/" + params.get("entry_point", "")]
    )
    tab.add_row(["Args", params.get("args", "")])
    tab.add_row(["GPUs", params.get("num_gpus", "")])
    tab.add_row(["CPUs", params.get("num_cpus_cores", "")])
    tab.add_row(["RAM", params.get("ram", "")])
    tab.add_row(["Walltime", params.get("walltime", "")])
    tab.add_row(["Base Image", params.get("base_image", "")])

    tab.align["Fields"] = "r"
    tab.align["Value"] = "l"
    print(tab)


if __name__ == "__main__":
    main()
