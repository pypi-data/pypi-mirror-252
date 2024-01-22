import argparse
import os
from clearml import Task
import sys
import bcrypt
import base64

from eml.utils.configs import EmlConfigs


def hashed_password(password):
    return base64.b64encode(bcrypt.hashpw(password.encode(), bcrypt.gensalt())).decode(
        "utf-8"
    )


def submit_task(password):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(dir_path, "defjob")
    os.chdir(template_path)

    task = Task.create(
        project_name=EmlConfigs().clearml_config["username"] + "/DevOps",
        task_name="change_password",
        task_type="",
        add_task_init_call=True,
        script="run_changepass.py",
        repo="",
        branch="",
        commit="",
        packages=["cython==0.29.36", "clearml", "tqdm", "pathspec", "eml"],
    )

    config = {}
    config["username"] = EmlConfigs().eml_config["username"]
    config["password"] = hashed_password(password)
    config["userid"] = EmlConfigs().eml_config["id"]
    task.connect(config)

    response = Task.enqueue(task=task, queue_name="service")
    if response.fields["status"] != "queued":
        print("Error submitting job to queue")
        return False

    print("Task {} sucessfully enqueued".format(task.id))
    return True


def main():
    current_folder = sys.argv.pop()
    os.chdir(current_folder)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--password",
        help="New password",
        required=True,
    )

    args = parser.parse_args()

    submit_task(args.password)


if __name__ == "__main__":
    main()
