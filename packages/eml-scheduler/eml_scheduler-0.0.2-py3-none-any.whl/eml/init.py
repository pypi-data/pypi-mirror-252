import os

file_path = "~/eml.conf"
file_path = os.path.expanduser(file_path)

if os.path.exists(file_path):
    with open(file_path, "r") as file:
        file_content = file.read()

    if "eml { " in file_content:
        print(
            "eml already configured. Please modify the eml section from eml.conf manually."
        )

    else:
        with open(file_path, "a") as file:
            file.write("eml { " + "\n")
            username = input("Type your username ")
            file.write('    "username" = "' + username + '"\n')
            file.write("}" + "\n")
