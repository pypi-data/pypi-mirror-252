import argparse
import yaml
import os
from clearml import Task
import sys
from datetime import datetime

from eml.utils.configs import EmlConfigs


def load_config(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    config["username"] = EmlConfigs().clearml_config["username"]
    config["task_name"] = datetime.now().strftime("%Y%m%d%H%M%S")
    return config


def submit_task(config, queue):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(dir_path, "defjob")
    os.chdir(template_path)

    task = Task.create(
        project_name=config["username"] + "/" + config["project_name"],
        task_name=config["task_name"],
        task_type=config["task_type"],
        add_task_init_call=True,
        script="run_docker.py",
        repo="",
        branch="",
        commit="",
        packages=["cython==0.29.36", "clearml", "tqdm", "pathspec", "eml-scheduler"],
    )

    task.connect(config)

    if config["num_gpus"] and config["num_gpus"] > 0:
        queue += ":gpu{}".format(int(config["num_gpus"])-1)
    response = Task.enqueue(task=task, queue_name=queue)
    if response.fields["status"] != "queued":
        print("Error submitting job to queue")
        return False

    print("Task {} sucessfully enqueued".format(task.id))
    return True


def validate_config(config):
    assert (
        len(config["walltime"].split(":")) == 4
    ), f"Walltime {config['walltime']} is not valid. It should be in the format DD:HH:MM:SS"
    for time in config["walltime"].split(":"):
        assert (
            time.isdigit()
        ), f"Walltime {config['walltime']} is not valid. It should be in the format DD:HH:MM:SS"
    assert int(config["num_gpus"]), f"Number of GPUs {config['num_gpus']} is not valid"
    assert int(
        config["num_cpus_cores"]
    ), f"Number of CPUs {config['num_cpus_cores']} is not valid"
    assert config["ram"][-1] in [
        "b",
        "k",
        "m",
        "g",
    ], f"RAM {config['ram']} is not valid. Please use a positive integer, followed by a suffix of b, k, m, g"
    assert int(
        config["ram"][:-1]
    ), f"RAM {config['ram']} is not valid. Please use a positive integer, followed by a suffix of b, k, m, g"


def main():
    current_folder = sys.argv.pop()
    os.chdir(current_folder)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--job",
        help="Path to the job file",
        required=True,
    )
    parser.add_argument(
        "--queue",
        help="Queue to submit the job",
        required=True,
    )
    args = parser.parse_args()
    path_jobfile = args.job
    if os.path.splitext(path_jobfile)[1] != ".yaml":
        path_jobfile += ".yaml"
    if not os.path.isabs(path_jobfile):
        path_jobfile = os.path.join(current_folder, path_jobfile)
    assert os.path.exists(path_jobfile), f"Job file {path_jobfile} does not exist"

    config = load_config(path_jobfile)
    validate_config(config)
    config["queue"] = args.queue
    submit_task(config, args.queue)


if __name__ == "__main__":
    main()
