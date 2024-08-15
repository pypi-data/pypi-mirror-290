# Copyright (c) 2023-2024 Contributors to the Eclipse Foundation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

"""Provides methods and functions to download and install dependencies."""

import os
import subprocess
import sys

ENV_VAR_VELOCITAS_OFFLINE = "VELOCITAS_OFFLINE"


def is_velocitas_offline_variant() -> bool:
    """Require and return an environment variable.

    Args:
        name (str): The name of the variable.

    Raises:
        ValueError: In case the environment variable is not set.

    Returns:
        str: The value of the variable.
    """
    offline_var = os.getenv(ENV_VAR_VELOCITAS_OFFLINE)
    if not offline_var or offline_var == "false":
        return False
    return True


def pip(args: list[str]) -> None:
    """Invoke the pip process with the given arguments."""
    subprocess.check_call([sys.executable, "-m", "pip", *args])


def install_requirements(requirements_path: str) -> None:
    """Install all required Python packages for the model generator and
    VSpec download."""
    if not is_velocitas_offline_variant():
        pip(["install", "-r", requirements_path])
