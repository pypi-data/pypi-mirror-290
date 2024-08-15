import datetime
import decimal
import json
import uuid
import enum
import attr
import cattrs


class JSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time/timedelta,
    decimal types, generators and other basic python objects.
    """

    def default(self, o):
        # For Date Time string spec, see ECMA 262
        # https://ecma-international.org/ecma-262/5.1/#sec-15.9.1.15
        if isinstance(o, datetime.datetime):
            return int(o.timestamp() * 1000)
        elif isinstance(o, (datetime.date, datetime.time)):
            return o.isoformat()
        elif isinstance(o, datetime.timedelta):
            return str(o.total_seconds())
        elif isinstance(o, (decimal.Decimal, uuid.UUID, enum.Enum)):
            return str(o)
        elif isinstance(o, bytes):  # Best-effort for binary blobs.
            return o.decode()
        elif hasattr(o, "tolist"):  # Numpy arrays and array scalars.
            return o.tolist()
        elif hasattr(o, "__getitem__"):
            cls = list if isinstance(o, (list, tuple)) else dict
            try:
                return cls(o)
            except Exception:  # noqa
                pass
        elif hasattr(o, "__iter__"):  # set, dict views, dict_keys, dict_values, etc.
            return tuple(item for item in o)
        elif hasattr(o, "__dict__"):  # Everything else
            data = o.__dict__.copy()
            for key, value in o.__class__.__dict__.items():
                if isinstance(value, property):
                    data[key] = getattr(o, key)
            return data
        elif attr.has(o):
            return cattrs.unstructure(o)
        else:
            raise ValueError("not supported data type")


def stringify(obj) -> str:
    """Convert object to JSON string"""
    return json.dumps(obj, cls=JSONEncoder)
