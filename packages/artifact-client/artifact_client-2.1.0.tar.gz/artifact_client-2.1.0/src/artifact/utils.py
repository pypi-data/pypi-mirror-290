import json
from typing import Any, Union, Callable, Optional


def format_body(body) -> str:
    if isinstance(body, str):
        # assume string is json formatted
        return body
    elif isinstance(body, dict) or isinstance(body, list):
        return json.dumps(body)
    elif isinstance(body, list):
        # allow list of objects
        return json.dumps([b.to_dict() if hasattr(body, "to_dict") else b for b in body])
    elif hasattr(body, "to_dict"):
        # assume body is a request object
        return json.dumps(body.to_dict())
    else:
        raise RuntimeError(f"Unsupported body type: {type(body)}")


def extract_body(resp):
    try:
        # responses with bodies have json method
        if hasattr(resp, "json") and callable(resp.json):
            return resp.json()
        # ApiException just has raw body
        elif hasattr(resp, "body"):
            # json can deserialize bytes or str
            return json.loads(resp.body)
    except Exception:
        raise ValueError(f"Only JSON bodies supported. Received: {resp.text if resp else 'None'}")


# copied from ozone-backend
def get_value(obj: Any, path: Union[str, list], default_value: Optional[Any] = None) -> Any:
    field_path = []
    if isinstance(path, list):
        field_path = path or []
    elif isinstance(path, str):
        field_path = path.split(".")
    # to ensure the value of the field is returned regardless of what it is,
    # as long as it exists, don't depend on truthiness of value, use a separate flag
    found_field = False
    for field_name in field_path:
        # each nested field must be found
        found_field = False
        if not field_name:
            return default_value
        if type(obj) is dict:
            if field_name in obj:
                found_field = True
                obj = {field_name: obj[field_name]}
            else:
                obj = None
                break
        elif hasattr(obj, field_name):
            found_field = True
            obj = getattr(obj, field_name)
        else:
            obj = None
            break
    if found_field:
        return obj
    else:
        # the default value might need to be calculated from another field that only exists
        # in the default case and therefore can only be evaluated at that time. therefore,
        # check to see if the default is callable, in which case execute it to calc the value.
        return default_value() if isinstance(default_value, Callable) else default_value
