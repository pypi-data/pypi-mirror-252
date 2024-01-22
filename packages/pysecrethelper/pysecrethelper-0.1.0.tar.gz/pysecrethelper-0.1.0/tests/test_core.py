import os
import unittest
from secrethelper import core
import pathlib

from ipydex import IPS, activate_ips_on_exception

activate_ips_on_exception()


# TODO: see https://setuptools.pypa.io/en/stable/userguide/datafiles.html#accessing-data-files-at-runtime
# from importlib.resources import files
# data_text = files('mypkg.data').joinpath('data1.txt').read_text()

data_dir = pathlib.Path(core.__file__).parents[0]
secrets_fpath = data_dir / "secrets-example.toml"

# hardcoded test password: DONT USE THIS IN PRODUCTION
TEST_PW = "QueeJ2go"


def get_static_input(prepared_input_list: list):
    input_idx = 0

    def static_input(msg=None):
        # msg will be accepted but ignored
        nonlocal input_idx

        res = prepared_input_list[input_idx % len(prepared_input_list)]
        input_idx += 1
        return res

    return static_input




# noinspection PyPep8Naming
class TestCore(unittest.TestCase):
    def setUp(self):
        os.environ[f"{core.PACKAGENAME}_UNITTEST"] = "True"

    def test_core1(self):
        test_string1 = 'echo "test works as expected"'
        test_string2 = 'echo "this also works"'

        static_input = get_static_input(
            prepared_input_list = [
                TEST_PW,
                test_string1,
                test_string2,
                "",  # empty string to quit input
            ]
        )

        res_list: list = core.create_encrypted_strings(print_res=False, __input_func=static_input)
        self.assertEqual(len(res_list), 2)
        res1, res2 = res_list
        crypter = core.get_crypter(pw=TEST_PW)

        res1_decrypted = crypter.decrypt(res1.encode("utf8")).decode("utf8")
        self.assertEqual(res1_decrypted, test_string1)

        res2_decrypted = crypter.decrypt(res2.encode("utf8")).decode("utf8")
        self.assertEqual(res2_decrypted, test_string2)

    def test_core2(self):
        res = core.get_decrypted_secret(section="commands", key="totp_unittest", secrets_fpath=secrets_fpath, pw=TEST_PW)
        self.assertEqual(res, 'oathtool -b --totp "FOO1234BAR"')
        res = core.get_decrypted_secret(section="commands", key="other_unittest", secrets_fpath=secrets_fpath, pw=TEST_PW)
        self.assertEqual(res, 'echo "general command" "with" --multiple -arguments')

    def test_core3__do_training(self):
        utc = core.UtContainer()

        static_input = get_static_input(
            prepared_input_list = [
                TEST_PW,
                "unittest_pw1",
                "wrong1",
                "wrong2",
                "wrong3",
                "unittest_pw1",
                "unittest_pw2",
                "",
            ]
        )

        core.do_training(10, secrets_fpath=secrets_fpath, __input_func=static_input, ut_container=utc)
        self.assertEqual(utc.idx, 4)
        self.assertEqual(utc.failed_tries["unittest2"], 3)

    def test_core4__cli(self):

        # test that the two commands are executable
        cmd = "secrethelper --version"
        res = os.system(cmd)
        self.assertEqual(res, 0)

        cmd = "secrettrainer --version"
        res = os.system(cmd)
        self.assertEqual(res, 0)
