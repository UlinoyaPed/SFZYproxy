import json
import logging as log
import subprocess
from typing import Tuple


def cmd(command, check=True, shell=True, capture_output=True, text=True):
    """
    Runs a command in a shell, and throws an exception if the return code is non-zero.
    :param command: any shell command.
    :return:
    """
    log.info(f" + {command}")

    return subprocess.run(command, check=check, shell=shell, capture_output=capture_output, text=text)


def po_token_verifier() -> Tuple[str, str]:
    token_object = generate_youtube_token()
    return token_object["visitorData"], token_object["poToken"]


def generate_youtube_token() -> dict:
    log.info("Generating YouTube token")
    result = cmd("youtube-po-token-generator")
    data = json.loads(result.stdout)
    log.info(f"Result: {data}")
    return data
