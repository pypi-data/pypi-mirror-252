"""
Core module of the sample project
"""

import os
import pathlib
import getpass
import subprocess
from cryptography.fernet import Fernet, InvalidToken
import hashlib
import base64
import random
from collections import defaultdict
import appdirs


from colorama import Style, Fore

import pyperclip

try:
    # this will be part of standard library for python >= 3.11
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


from ipydex import IPS, activate_ips_on_exception

activate_ips_on_exception()

PACKAGENAME = __name__.split(".")[0]

DATADIR_PATH = pathlib.Path(appdirs.user_data_dir(appname=PACKAGENAME))
SECRETS_FPATH = DATADIR_PATH / "secrets.toml"


class UtContainer:
    def __init__(self):
        self.failed_tries = defaultdict(lambda: 0)
        idx = 0


def get_crypter(pw=None, __input_func=None):
    if pw is None:
        if __input_func is not None:
            input_func = __input_func
        else:
            input_func = getpass.getpass
        pw = input_func()
    else:
        # explicitly providing a password is only allowed in unittest mode
        varname = f"{PACKAGENAME}_UNITTEST"
        assert os.getenv(varname) == "True"

    # Fernet key must be 32 url-safe base64-encoded bytes
    # -> generate hash (byte string) from password, trim it to length 32 and encode it
    enc_key = base64.urlsafe_b64encode(hashlib.sha256(pw.encode("utf8")).digest()[:32])
    crypter = Fernet(enc_key)

    return crypter


def create_encrypted_strings(print_res=True, pw=None, __input_func=None):

    crypter = get_crypter(pw, __input_func=__input_func)

    if __input_func is not None:
        input_func = __input_func
    else:
        input_func = input

    res_list = []

    while True:
        orig_str = input_func("enter string to encrypt (empty string to quit): ")
        if orig_str == "":
            break
        res = crypter.encrypt(orig_str.encode("utf8")).decode("utf8")
        if print_res:
            pyperclip.copy(res)
            print(f"{res}  (copied to clipboard)")
        res_list.append(res)
    return res_list


def get_secret_data(secrets_fpath, section=None) -> dict:
    if secrets_fpath is None:
        secrets_fpath = SECRETS_FPATH

    with open(secrets_fpath, "rb") as fp:
        data = tomllib.load(fp)

    if section is None:
        return data

    if section not in data:
        print(bred(f" unknown section '{section}' in {secrets_fpath}"))
        exit(1)

    data_section = data[section]
    return data_section


def get_decrypted_secret(section, key, secrets_fpath=None, pw=None):
    assert isinstance(section, str)
    data_section = get_secret_data(secrets_fpath=secrets_fpath, section=section)

    if key not in data_section:
        print(bred(f" unknown key '{key}' for section '{section}' in {secrets_fpath}"))
        exit(1)

    data_entry = data_section[key]
    crypter = get_crypter(pw)

    try:
        decrypted_data_entry = crypter.decrypt(data_entry.encode("utf8")).decode("utf8")
    except InvalidToken:
        print(bred("wrong password"))
        exit(2)

    return decrypted_data_entry


def get_cmd_output(cmd: str, copy_to_cb=False):
    res = subprocess.run(cmd, capture_output=True)
    code = res.stdout.decode("utf8").replace("\n", "")
    if copy_to_cb:
        pyperclip.copy(code)
    return code


def _run_command_command(section, key, secrets_fpath=None, pw=None):
    cmd = get_decrypted_secret(section=section, key=key, secrets_fpath=secrets_fpath, pw=pw)
    code = get_cmd_output(cmd=cmd.replace('"', "").split(" "), copy_to_cb=True)
    print(f"{code}    (copied to clipboard)")


def decrypt_and_run_command(key, secrets_fpath=None, pw=None):
    return _run_command_command(section="commands", key=key, secrets_fpath=secrets_fpath, pw=pw)


def get_salted_hash(salt: str, src_str):
    src_bytes = f"{salt}{src_str}".encode("utf8")
    hex_digest = hashlib.sha256(src_bytes).hexdigest()
    return hex_digest


def create_training_data():
    salt = input("salt: ")
    while True:
        print("Enter password to train (will be displayed); empty string to quit")
        pw = input()
        if pw == "":
            break
        hex_digest = get_salted_hash(salt, pw)
        pyperclip.copy(hex_digest)
        print(f"{hex_digest}  (copied to clipboard)\n\n")


def do_training(rounds: int, secrets_fpath=None, __input_func=None, ut_container=None):
    training_data = get_secret_data(secrets_fpath=secrets_fpath, section="training")
    training_items = list(training_data.items())
    if __input_func is not None:
        # this allows to unittest this otherwise interactive function
        input_fnc = __input_func

    else:
        # shuffling when not in unittest
        random.shuffle(training_items)
        input_fnc = getpass.getpass

    if ut_container is None:
        ut_container = UtContainer()

    correct_counter = 0
    L = len(training_items)
    idx = 0

    print("\nTrain memorized secrets by comparing their hash to stored value.")
    print("Use empty string to abort.\n")

    salt = input_fnc(f"{'salt'}: ")
    if salt == "":
        # end training for empty user input
        return

    while correct_counter < rounds:
        key, hash = training_items[idx % L]

        attempt = 0
        max_attempts = 3
        while attempt < max_attempts:
            user_input = input_fnc(f"{key}: ")
            if user_input == "":
                # end training for empty user input
                return
            hex_digest = get_salted_hash(salt, user_input)

            if hex_digest == hash:
                print(bgreen("✓"), end="")
                correct_counter += 1
                break
            else:
                attempt += 1
                ut_container.failed_tries[key] += 1
                print(bred("✗"), end="")
        idx += 1
        # store overall rounds for unittest
        ut_container.idx = idx
        space = " " * (max_attempts - attempt + 1 + 1 * (max_attempts == attempt))
        print(space, f"  Stats: {correct_counter}/{rounds} correct\n")


def bootstrap_data():
    local_dir = pathlib.Path(__file__).parents[0]
    example_fpath = local_dir / "secrets-example.toml"
    assert os.path.isfile(example_fpath)
    os.makedirs(DATADIR_PATH, exist_ok=True)

    if os.path.isfile(SECRETS_FPATH):
        print(yellow("Caution:"), f"File already exists: {SECRETS_FPATH}")
        res = input("Overwrite? [yes/N/no] ")
        if res.lower() != "yes":
            print("abort")
            return

    with open(example_fpath, "rb") as fp:
        lines = fp.readlines()

    # adapt comment in the first line
    lines[0] = (
        # fmt: skip
        b"# This file was generated from `secrets-example.toml`.\n"
        b"# See docs on how to insert your own secrets.\n"
    )
    with open(SECRETS_FPATH, "wb") as fp:
        fp.writelines(lines)

    print(f"File written: {SECRETS_FPATH}")


def edit_data(editor):
    if editor == "__None__":
        editor = os.getenv("EDITOR", None)
    if editor is None:
        print(bred("Environment variable `EDITOR` seems not to be set. Please specify editor via commandline"))

    cmd = f"{editor} {SECRETS_FPATH}"
    res = input(f"Execute the command: `{cmd}`? [y/N] ")
    if res.lower() not in ("y", "yes"):
        print("abort")
        exit()
    os.system(cmd)


def bright(txt):
    return f"{Style.BRIGHT}{txt}{Style.RESET_ALL}"


def bgreen(txt):
    return f"{Fore.GREEN}{Style.BRIGHT}{txt}{Style.RESET_ALL}"


def bred(txt):
    return f"{Fore.RED}{Style.BRIGHT}{txt}{Style.RESET_ALL}"


def yellow(txt):
    return f"{Fore.YELLOW}{txt}{Style.RESET_ALL}"
