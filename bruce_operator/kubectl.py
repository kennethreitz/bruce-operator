import json

import logme
import delegator


@logme.log
def kubectl(cmd, as_json=True, raise_on_error=True, logger=None):
    json_flag = "-o=json" if as_json else ""
    cmd = f"kubectl {cmd} {json_flag}"

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
