import os
import json

import logme
import delegator

from .env import TOKEN_LOCATION, IN_KUBERNETES, CERT_LOCATION


@logme.log
def kubectl(cmd, as_json=True, raise_on_error=True, logger=None):
    json_flag = "-o=json" if as_json else ""
    # if IN_KUBERNETES:
    #     host = os.environ["KUBERNETES_SERVICE_HOST"]
    #     port = os.environ["KUBERNETES_SERVICE_PORT"]
    #     with open(TOKEN_LOCATION, "r") as f:
    #         token = f.read()
    #     server_flag = f"--server=https://{host}:{port} --token={token} --certificate-authority={CERT_LOCATION}"
    # else:
    #     server_flag = ""
    # cmd = f"kubectl {json_flag} {server_flag} {cmd}"
    cmd = f"kubectl {json_flag} {cmd}"

    logger.debug(f"$ {cmd}")
    c = delegator.run(cmd)

    if as_json:
        try:
            assert c.ok
            return json.loads(c.out)
        except AssertionError as e:
            logger.debug("Failed!")
            logger.debug(c.out)
            logger.debug(c.err)
            if not raise_on_error:
                return c
            else:
                raise e
    else:
        return c
