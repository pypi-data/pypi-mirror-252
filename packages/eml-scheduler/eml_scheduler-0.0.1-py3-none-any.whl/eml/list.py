import argparse
from tqdm import tqdm
from clearml import Task
from prettytable import PrettyTable

from eml.utils.configs import EmlConfigs


def get_tasks(project_name, tags, status):
    if project_name is None:
        project_name = ""
    config = EmlConfigs()
    username = config.clearml_config["username"]
    task_filter = {
        "user": [config.eml_config["id"]],
        "order_by": ["-last_update"],
    }
    if status:
        task_filter["status"] = [status]
    tasks = Task.get_tasks(
        project_name=username + "/" + project_name,
        tags=tags,
        task_filter=task_filter,
    )
    return tasks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project",
        help="Project name",
    )
    parser.add_argument(
        "--tags",
        help="Filter by tags",
    )
    parser.add_argument(
        "--status",
        help="Filter by status",
    )
    args = parser.parse_args()

    tasks = get_tasks(args.project, args.tags, args.status)

    tab = PrettyTable(["ID", "Project", "Status", "Created", "Last Update"])
    for t in tqdm(tasks, leave=False, desc="Fetching tasks"):
        project_name = t.get_project_name().split("/")
        if len(project_name) > 1:
            project_name = "/".join(project_name[1:])

        tab.add_row(
            [
                t.id,
                project_name,
                t.status,
                t.data.created.strftime("%d/%m/%Y, %H:%M:%S"),
                t.data.last_update.strftime("%d/%m/%Y, %H:%M:%S"),
            ]
        )
    print(tab)


if __name__ == "__main__":
    main()
