#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# === This file is part of Calamares - <http://github.com/calamares> ===
#
#   Copyright 2015, Teo Mrnjavac <teo@kde.org> #   Copyright 2017. Alf Gaida <agaida@siduction.org>
#
#   Calamares is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Calamares is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Calamares. If not, see <http://www.gnu.org/licenses/>.

import subprocess
import libcalamares
import os


def run():
    """
    Remove live user from target system
    """
    username = libcalamares.job.username
    try:
        libcalamares.utils.check_target_env_call(["systemctl", "enable",
                                                  "autologin@{}".format(username)])
    except subprocess.CalledProcessError as e:
        libcalamares.utils.debug("Cannot configure autologin.",
                                 "'systemctl' terminated with exit code",
                                 "{}.".format(e.returncode))
    try:
        libcalamares.utils.check_target_env_call(["freshclam"])
    except subprocess.CalledProcessError as e:
        libcalamares.utils.debug("Cannot update clam database.",
                                 "'freshclam' terminated with exit code",
                                 "{}.".format(e.returncode))

