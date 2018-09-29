import json


import delegator


def kubectl(cmd, as_json=True, raise_on_error=True):
    json_flag = "-o=json" if as_json else ""
    cmd = f"kubectl {cmd} {json_flag}"

    c = delegator.run(cmd)

    if as_json:
        try:
            assert c.ok
            return json.loads(c.out)
        except AssertionError as e:
            if not raise_on_error:
                return c
            else:
                raise e
    else:
        return c
