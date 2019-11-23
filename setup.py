#!/usr/bin/env python

import os
import sys

import setuptools


def _gen_console_scripts():
    yield "easy_install = setuptools.command.easy_install:main"

    # Gentoo distributions manage the python-version-specific scripts
    # themselves, so those platforms define an environment variable to
    # suppress the creation of the version-specific scripts.
    var_names = (
        'SETUPTOOLS_DISABLE_VERSIONED_EASY_INSTALL_SCRIPT',
        'DISTRIBUTE_DISABLE_VERSIONED_EASY_INSTALL_SCRIPT',
    )
    if any(os.environ.get(var) not in (None, "", "0") for var in var_names):
        return
    tmpl = "easy_install-{shortver} = setuptools.command.easy_install:main"
    yield tmpl.format(shortver='{}.{}'.format(*sys.version_info))


if __name__ == "__main__":
    setuptools.setup(
        use_scm_version=True,
        entry_points={
            "console_scripts": list(_gen_console_scripts()),
            "setuptools.installation": ['eggsecutable = easy_install:bootstrap'],
        },
    )
