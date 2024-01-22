import argparse
import yaml
from datetime import datetime
import os
import sys


def default_job(
    project_name="default",
    entry_point="",
    working_dir="./",
):
    if not entry_point:
        entry_point = ""

    return {
        "project_name": project_name,
        "task_file_created": datetime.now().strftime("%Y%m%d%H%M%S"),
        "tags": [],
        "task_type": "training",
        "working_dir": working_dir,
        "entry_point": entry_point,
        "args": "",
        "num_gpus": 1,
        "num_cpus_cores": 32,
        "ram": "4g",
        "walltime": "0:24:00:00",
        "base_image": "eml/cuda:11.6.1-base-ubuntu20.04",
    }


def create_file(args, current_folder):
    job = default_job(
        args.project,
        args.script,
        current_folder,
    )
    yaml.dump(job, open(os.path.join(current_folder, f"{args.job}.yaml"), "w"))


def main():
    current_folder = sys.argv.pop()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--job",
        help="Name of the job to be created. If not provided, a timestamp will be used as the job name.",
    )
    parser.add_argument(
        "--project",
        help='Name of the project to be created. Default value is "default"',
        default="default",
    )
    parser.add_argument(
        "--script",
        help="Entry point for the job. This argument is required.",
        required=True,
    )

    args = parser.parse_args()
    if not args.job:
        args.job = datetime.now().strftime("%Y%m%d%H%M%S")
    create_file(args, current_folder)


if __name__ == "__main__":
    main()
