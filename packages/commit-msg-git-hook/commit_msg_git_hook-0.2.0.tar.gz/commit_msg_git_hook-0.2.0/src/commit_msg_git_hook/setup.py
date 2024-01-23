import os
import subprocess
import sys

CONFIG_FILE_NAME = "commit-msg.config.json"
GIT_HOOKS_DIRECTORY = "./.github/git-hooks"

os.makedirs(GIT_HOOKS_DIRECTORY, exist_ok=True)

subprocess.run(["git", "config", "core.hooksPath", GIT_HOOKS_DIRECTORY])

if not os.path.exists(f"{GIT_HOOKS_DIRECTORY}/commit-msg"):
    commit_msg_hook_file = open(f"{GIT_HOOKS_DIRECTORY}/commit-msg", "w")
    commit_msg_hook_file.writelines(
        [
            "#!/usr/bin/env python3\n\n",
            "from commit_msg_git_hook import commit_msg as cm\n\n",
            "cm.main()\n",
        ]
    )
    commit_msg_hook_file.close()

    if sys.platform.startswith('linux'):
        subprocess.run(["chmod", "+x", f"{GIT_HOOKS_DIRECTORY}/commit-msg"])

if not os.path.exists(CONFIG_FILE_NAME):
    config_file = open(CONFIG_FILE_NAME, "w")
    config_file.writelines(
        [
            '{\n',
            '    "enabled": true,\n',
            '    "revert": true,\n',
            '    "max_length": 72,\n',
            '    "types": [\n',
            '        "build",\n',
            '        "ci",\n',
            '        "docs",\n',
            '        "feat",\n',
            '        "fix",\n',
            '        "perf",\n',
            '        "refactor",\n',
            '        "style",\n',
            '        "test",\n',
            '        "chore"\n',
            '    ],\n',
            '    "scopes": []\n',
            '}\n',
        ]
    )
    config_file.close()
