# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Python language helper classes and functions."""

# Standard Library
import inspect
from typing import Any, Callable, Dict, List, Optional


def get_inner_classes(cls: type, parent_class: Optional[type] = None) -> List[type]:
    """Get the inner classes of the given class.

    Optional condition it that the inner classes are subclasses of the given parent class.

    Args:
        cls: Class to get subclasses for.
        parent_class: Class type that subclasses must be child classes to.
    """
    return [
        getattr(cls, name)
        for name in dir(cls)
        if isinstance(getattr(cls, name), type)
        and getattr(cls, name).__module__ == cls.__module__
        and (parent_class is None or issubclass(getattr(cls, name), parent_class))
    ]


def get_nested_dict(dict_obj: Dict[str, Any], key_list: List[str]) -> Dict[str, Any]:
    """Retrieve a nested dictionary by following a list of keys.

    Args:
        dict_obj: Dictionary to get the nested dict from.
        key_list: List of key values that specify the root of the nested dict to return.
    """
    current = dict_obj
    for key in key_list:
        # Use get to avoid KeyError if key is not present
        current = current.get(key)  # type: ignore
        if not isinstance(current, dict):
            raise ValueError(
                f"Value of final key is not a dictionary. Key: {key}, Value: {current}"
            )
    return current


def get_function_arg_names(func: Callable[..., Any]) -> List[str]:
    """Inspect the given function and return the argument names as a list."""
    arg_names = [
        param.name for param in inspect.signature(func).parameters.values() if param.name != "self"
    ]
    return arg_names


def what_file_called_me() -> str:
    """Determine what file a function is called from.

    Example:
        foo.py

        def foo():
            bar()

        bar.py

        def bar():
            print(f"The file that called me is {what_file_called_me()}")

        $ python foo.py
        >  The file that called me is foo.py
    """
    # Start from the current frame
    current_frame = inspect.currentframe()
    # Move back to the caller's caller's frame
    if current_frame is not None:
        caller_frame = current_frame.f_back
        if caller_frame is not None:
            caller_caller_frame = caller_frame.f_back
            if caller_caller_frame is not None:
                # Get the file name from the caller's caller's frame
                callers_filename = caller_caller_frame.f_code.co_filename
                return callers_filename

    raise RuntimeError("Unable to get file of caller.")
