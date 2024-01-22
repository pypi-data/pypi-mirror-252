import os
import argparse

from . import core, release


def main():
    parser = argparse.ArgumentParser(description=f"cli tool to handle secrets; data taken from {core.SECRETS_FPATH}")

    parser.add_argument("--encrypt", "-e", help=f"prompt for password; prompt for string, display and copy encrypted string; repeat", action="store_true")

    parser.add_argument("--decrypt", "-d", help=f"run command identified by key; print and copy output", metavar="key")

    add_common_options(parser)
    args = parser.parse_args()

    if args.encrypt:
        core.create_encrypted_strings()
        return
    elif args.decrypt:
        core.decrypt_and_run_command(args.decrypt)
        return
    if handle_common_options(parser, args):
        return

    parser.print_help()


def add_common_options(parser):
    """
    Add command line options which are used for both scripts.
    """
    parser.add_argument("--version", help="print version and exit", action="store_true")

    parser.add_argument(
        "--bootstrap-data", "-b", help="create initial version of data file (secrets.toml)", action="store_true"
    )

    parser.add_argument(
        "--edit-data",
        "-ed",
        help="open data file (secrets.toml) in specified or default editor",
        nargs="?",
        metavar="EDITOR",
        const="__None__",
        default=None,
    )


def handle_common_options(parser, args):
    match = True

    if args.bootstrap_data:
        core.bootstrap_data()
    elif args.version:
        print(release.__version__)
    elif args.edit_data:
        core.edit_data(args.edit_data)
    else:
        match = False
    return match


def do_training():
    parser = argparse.ArgumentParser(
        description=f"cli tool to train memorization of secrets; data taken from {core.SECRETS_FPATH}"
    )

    parser.add_argument(
        "--create-training-data", "-ctd", help=f"prompt for passwords and create salted hashes", action="store_true"
    )

    add_common_options(parser)
    args = parser.parse_args()

    if handle_common_options(parser, args):
        return
    elif args.create_training_data:
        core.create_training_data()

    core.do_training(rounds=10)
