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
    parser.add_argument(
        "-y",
        help="Automatically accept deletion",
        action="store_true",
    )
    args = parser.parse_args()

    t = get_task(args.id)
    if not t:
        print("Task not found")
        return

    tab = PrettyTable(["Fields", "Value"])
    tab.add_row(["ID", t.id])
    tab.add_row(["Project", t.get_project_name()])
    tab.add_row(["Status", t.status])
    tab.add_row(["Last Update", t.data.last_update.strftime("%d/%m/%Y, %H:%M:%S")])
    tab.align["Fields"] = "r"
    tab.align["Value"] = "l"
    print(tab)

    if not args.y:
        ans = input("Are you sure you want to delete this task? (y/N) ")
        if ans.lower() != "y":
            print("Aborting deletion")
            return

    t.delete()


if __name__ == "__main__":
    main()
