# Copyright (c) Huawei Technologies Co., Ltd. 2024. All rights reserved.
import re
from collections import OrderedDict
from functools import wraps

ORDERED_DICT = OrderedDict({"on huggingface.co": "on openmind.cn",
                            "Hugging Face": "openMind",
                            "hf.co": "openmind.cn",
                            "HF google": "openMind",
                            })


def warning_wrapper(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        msg = args[0]
        if len(args) >= 2 and isinstance(msg, str) and isinstance(args[1], Warning):
            replace_dict = ORDERED_DICT
            replace_dict = dict((re.escape(k), v) for k, v in replace_dict.items())
            pattern = re.compile("|".join(replace_dict.keys()))
            filtered_msg = pattern.sub(lambda m: replace_dict[re.escape(m.group(0))], msg)
            new_args = {filtered_msg}
            for i in range(1, len(args)):
                new_args.add(args[i])
            wrapped_args = tuple(new_args)
            return fn(*wrapped_args, **kwargs)
        return fn(*args, **kwargs)

    return wrapper
