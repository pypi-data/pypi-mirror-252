[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Secrethelper

Simple command line utility for handling secrets.

**Important:** USE AT YOUR OWN RISK!

## Use Case 1

Some commands are needed frequently but they contain secrets. Examples:

- `oathtool -b --totp "PV3YEM43I22ISNWK"` (based on a secret key create a time based one time password for **2FA**)
- `git pull https://some.user%40host.org:foo-bar-password@git.myservice.com/reponame` (git connection via https without being prompted for a password)

Obviously, it is insecure to store them unencrypted on your system (e.g. in your command history).

Solution: `secrethelper` reads a data file (`secrets.toml`) which contains **encrypted** versions of such commands, prompts for a password decrypts the relevant command, executes it and displays the result (and copies it into the clipboard). The actual **secret is never shown**.

## Use Case 2

Some secrets (e. g.passwords) are important to memorize, but are needed only rarely. Thus, there are only few occations to practise them.

Solution: `secrettrainer` reads a data file (`secrets.toml`) which contains the (salted) hashes of such passwords. During a trainig session you are propted for some of them the correctness is determined by comparing the hashes.

## Usage

### `secrethelper`

- `secrethelper --help`: Show help.
    - short version: `-h`
- `secrethelper --bootstrap-data`: Create `secrets.toml` in suitable place. Example: `~/.local/share/secrethelper/` (depends on OS). The content is based on [`src/secrethelper/secrets-example.toml`](src/secrethelper/secrets-example.toml).
    - short version: `-b`
- `secrethelper --edit-data`: Open `secrets.toml` in the default editor.
    - short version: `-ed`
- `secrethelper --edit-data [EDITOR]`: Open `secrets.toml` in the specified editor.
    - short version: `-ed [EDITOR]`
    - example: `--edit-data codium`
- `secrethelper --encrypt`: Prompt for password, then prompt for some arbitrary string. Disyplay the encrypted version of the string (also copied to the clipboard). This string can be pasted directly in `secrets.toml`
- `secrethelper --decrypt-and-execute [key]`: Prompt for password, extract the encrypted command from `secrets.toml`, execute it and disyplay the result (also copied to the clipboard).
    - short version: `-d [key]`

### `secrettrainer`

- `secrettrainer --help`: Show help.
    - short version: `-h`
- `secrettrainer --create-training-data`: Create training data: Prompt for password (salt), prompt for secret and display salted hash of the secret (also copied to clipboard). This string can be pasted directly in `secrets.toml` in section `[training]`. An empty string quits the process.
    - short version: `-ctd`
- `secrettrainer` (no options/arguments): Create a suffled list of keys from section `[training]`, prompt for password (used as salt for hash), prompt for secrets, compare hash display ✓ or ✗. Train 10 rounds. Empty string quits this process.



## Installation and Preparation

### In first terminal:
- `pip install pysecrethelper`: Install the software.
- `secrethelper -b`  Bootstrap data file `secrets.toml`.
- `secrethelper -ed`  Open `secrets.toml` in default editor.

### In another terminal:
- `secrethelper -e`: Create and copy encrypted string → you can paste it into `secret.toml` in section `[commands]`. This is for use case 1 (see above).
- `secrethelper -ctd`: Create hashes and copy salted hashes for training → you can paste it into `secret.toml` in section `[training]`. This is for use case 2 (see above).
