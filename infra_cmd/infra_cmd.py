import subprocess
import logging
import sys
import time
import yaml
import tempfile
import os

from pathlib import Path

log = logging.getLogger()
log.setLevel(logging.DEBUG)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
log.addHandler(stream)


def send_cmd(cmd=None, print_cmd=True, print_output=True):
    if print_cmd:
        logging.info(cmd)
    returned_text = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    if print_output:
        logging.info(returned_text)
    return returned_text


def wait_expected_result(
    sleep=10, timeout=100, cmd=None, expected_string=None, expected_error=None
):
    if expected_error is None:
        expected_error = "timeout should be larger than sleep time"
    while True:
        returned_text = send_cmd(cmd)
        if expected_string in returned_text:
            return True
        time.sleep(sleep)
        timeout -= sleep
        if timeout < sleep:
            raise ValueError(expected_error)


def yaml_to_dict(path=None):
    full_path = os.path.join(Path(__file__).parent.parent, path)
    with open(full_path, "r") as file:
        res = yaml.load(file.read(), Loader=yaml.Loader) or {}
        if not isinstance(res, dict):
            raise ValueError(f"Invalid yaml file")
        return res


def dict_to_yaml(data=None):
    temp_folder = tempfile.mkdtemp()
    path = os.path.join(temp_folder, "data.yaml")
    with open(path, "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
    return path
