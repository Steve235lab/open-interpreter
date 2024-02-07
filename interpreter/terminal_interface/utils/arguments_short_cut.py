import argparse

import pkg_resources

from ...core.core import OpenInterpreter
from ..profiles.profiles import open_profile_dir, reset_profile


shortcut_arguments = [
    {
        "name": "reset_profile",
        "help_text": "reset a profile file. run `--reset_profile` without an argument to reset all default profiles",
        "type": str,
        "default": "NOT_PROVIDED",
        "nargs": "?",  # This means you can pass in nothing if you want
    },
    {"name": "profiles", "help_text": "opens profiles directory", "type": bool},
    {
        "name": "version",
        "help_text": "get Open Interpreter's version number",
        "type": bool,
    },
]


# Deal with arguments don't need llm to work
def arguments_shortcut():
    parser = argparse.ArgumentParser(description="Open Interpreter")
    # Add arguments
    for arg in shortcut_arguments:
        action = arg.get("action", "store_true")
        nickname = arg.get("nickname")
        default = arg.get("default")

        if arg["type"] == bool:
            if nickname:
                parser.add_argument(
                    f"-{nickname}",
                    f'--{arg["name"]}',
                    dest=arg["name"],
                    help=arg["help_text"],
                    action=action,
                    default=default,
                )
            else:
                parser.add_argument(
                    f'--{arg["name"]}',
                    dest=arg["name"],
                    help=arg["help_text"],
                    action=action,
                    default=default,
                )
        else:
            choices = arg.get("choices")

            if nickname:
                parser.add_argument(
                    f"-{nickname}",
                    f'--{arg["name"]}',
                    dest=arg["name"],
                    help=arg["help_text"],
                    type=arg["type"],
                    choices=choices,
                    default=default,
                    nargs=arg.get("nargs"),
                )
            else:
                parser.add_argument(
                    f'--{arg["name"]}',
                    dest=arg["name"],
                    help=arg["help_text"],
                    type=arg["type"],
                    choices=choices,
                    default=default,
                    nargs=arg.get("nargs"),
                )

    args = parser.parse_args()

    if args.profiles:
        open_profile_dir()
        return

    if args.reset_profile != "NOT_PROVIDED":
        reset_profile(
            args.reset_profile
        )  # This will be None if they just ran `--reset_profile`
        return

    if args.version:
        version = pkg_resources.get_distribution("open-interpreter").version
        update_name = "New Computer Update"  # Change this with each major update
        print(f"Open Interpreter {version} {update_name}")
        return

    return OpenInterpreter()
