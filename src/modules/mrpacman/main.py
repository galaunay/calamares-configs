#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# === This file is part of Calamares - <http://github.com/calamares> ===
#
#   Copyright 2014, Pier Luigi Fiorini <pierluigi.fiorini@gmail.com> [packages]
#   Copyright 2016, Mike Krüger <mikekrueger81@gmail.com> [mrpacman]
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

import libcalamares
import urllib.request
from libcalamares.utils import check_target_env_call, target_env_call


class PackageManager:

    """ Package manager class.

    :param backend:
    """

    def __init__(self, backend):
        self.backend = backend

    def install(self, pkgs, from_local=False):
        """ Installs packages.

        :param pkgs:
        :param from_local:
        """

        if self.backend == "pacman":
            if from_local:
                pacman_flags = "-U"
            else:
                pacman_flags = "-Sy"

            check_target_env_call(["pacman", pacman_flags, "--noconfirm"
                                  ] + pkgs)

    def remove(self, pkgs):
        """ Removes packages.

        :param pkgs:
        """

        if self.backend == "pacman":
            check_target_env_call(["pacman", "-Rs", "--noconfirm"]
                                  + pkgs)

    def upgrade(self):
        """ upgrades all packages.

        """

        if self.backend == "pacman":
            check_target_env_call(["pacman", "-Syyu", "--noconfirm"])


def connected(reference):
    try:
        urllib.request.urlopen(reference, timeout=1)
        return True
    except urllib.request.URLError:
        return False


def run_operations(pkgman, entry):
    """ Call package manager with given parameters.

    :param pkgman:
    :param entry:
    """

    for key in entry.keys():
        if key == "install":
            pkgman.install(entry[key])
        elif key == "remove":
            pkgman.remove(entry[key])
        elif key == "localInstall":
            pkgman.install(entry[key], from_local=True)


def run():
    """ Calls routine with detected package manager to install locale packages
    or remove drivers not needed on the installed system.

    :return:
    """

    backend = libcalamares.job.configuration.get("backend")

    if backend not in ("pacman"):
        return "Bad backend", "backend=\"{}\"".format(backend)

    pkgman = PackageManager(backend)
    operations = libcalamares.job.configuration.get("operations", [])

    for entry in operations:
        run_operations(pkgman, entry)

    if connected("http://google.com"):
        pkgman.upgrade()

    if libcalamares.globalstorage.contains("packageOperations"):
        run_operations(pkgman,
                       libcalamares.globalstorage.value("packageOperations"
                       ))

    return None
