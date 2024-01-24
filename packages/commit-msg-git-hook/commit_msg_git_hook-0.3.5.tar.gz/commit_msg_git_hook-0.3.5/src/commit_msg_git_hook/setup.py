import os
import subprocess
import sys
import importlib.resources as res


CONFIG_FILE_NAME = "commit-msg.config.json"
GIT_HOOKS_DIRECTORY = "./.github/git-hooks"

SUPPORTED_OS_TYPES = {
    "linux": "Linux",
    "darwin": "macOS",
    "win32": "Windows",
}


def get_os_type():
    os_type = sys.platform

    for supported_os_key in SUPPORTED_OS_TYPES:
        if os_type.startswith(supported_os_key):
            os_type = supported_os_key
            break

    return os_type


def show_os_type(os_type):
    print(f'Your OS type is "{SUPPORTED_OS_TYPES.get(os_type, os_type)}".\n')


def create_git_hook_from_template(os_type: str):
    if not os.path.exists(f"{GIT_HOOKS_DIRECTORY}/{os_type}/commit-msg"):
        template = (
            res.files("commit_msg_git_hook") / "templates" / os_type / "commit-msg"
        )
        template_file = template.open()

        commit_msg_hook_file = open(f"{GIT_HOOKS_DIRECTORY}/{os_type}/commit-msg", "w")
        commit_msg_hook_file.write(template_file.read())

        commit_msg_hook_file.close()
        template_file.close()


def create_git_hooks(os_type):
    for supported_os_key in SUPPORTED_OS_TYPES.keys():
        os.makedirs(f"{GIT_HOOKS_DIRECTORY}/{supported_os_key}", exist_ok=True)

        create_git_hook_from_template(supported_os_key)

    if os_type == "linux":
        subprocess.run(["chmod", "+x", f"{GIT_HOOKS_DIRECTORY}/{os_type}/commit-msg"])


def git_config_core_hooks_path(os_type: str):
    subprocess.run(
        ["git", "config", "core.hooksPath", f"{GIT_HOOKS_DIRECTORY}/{os_type}"]
    )


def create_config_file():
    if not os.path.exists(CONFIG_FILE_NAME):
        template = res.files("commit_msg_git_hook") / "templates" / CONFIG_FILE_NAME
        template_file = template.open()

        config_file = open(CONFIG_FILE_NAME, "w")
        config_file.write(template_file.read())

        config_file.close()
        template_file.close()


if __name__ == "__main__":
    os_type = get_os_type()

    show_os_type(os_type)
    if os_type not in SUPPORTED_OS_TYPES.keys():
        print("ERROR: Your OS type is currently unsupported.")
        exit(1)

    create_git_hooks(os_type)
    git_config_core_hooks_path(os_type)
    create_config_file()

    print(
        f"Success: commit-msg git-hook configured for {SUPPORTED_OS_TYPES[os_type]}.\n"
    )
