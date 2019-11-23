"""Run the EasyInstall command"""

import sys
import os
import textwrap
import contextlib


def bootstrap():
    # This function is called when setuptools*.egg is run using /bin/sh
    import setuptools

    argv0 = os.path.dirname(setuptools.__path__[0])
    sys.argv[0] = argv0
    sys.argv.append(argv0)
    main()


def main(argv=None, **kw):
    from setuptools import setup
    from setuptools.dist import Distribution

    class DistributionWithoutHelpCommands(Distribution):
        common_usage = ""

        def _show_help(self, *args, **kw):
            with _patch_usage():
                Distribution._show_help(self, *args, **kw)

    if argv is None:
        argv = sys.argv[1:]

    with _patch_usage():
        setup(
            script_args=['-q', 'easy_install', '-v'] + argv,
            script_name=sys.argv[0] or 'easy_install',
            distclass=DistributionWithoutHelpCommands,
            **kw
        )


@contextlib.contextmanager
def _patch_usage():
    import distutils.core

    USAGE = textwrap.dedent(
        """
        usage: %(script)s [options] requirement_or_url ...
           or: %(script)s --help
        """
    ).lstrip()

    def gen_usage(script_name):
        return USAGE % dict(script=os.path.basename(script_name))

    saved = distutils.core.gen_usage
    distutils.core.gen_usage = gen_usage
    try:
        yield
    finally:
        distutils.core.gen_usage = saved


if __name__ == '__main__':
    from setuptools.command import easy_install

    easy_install.main()
