#!/usr/bin/env python3

"""
** Alias for ``cutcutcodec.testing.run`` **
-------------------------------------------
"""

import sys

import click



@click.command()
@click.option("--light", is_flag=True, help="Performs only some light tests.")
def main(light: bool=False) -> int:
    """
    Checks if the installation is correct, alias to ``cutcutcodec-test``.
    """
    from cutcutcodec.testing.run import run_tests # no global import for cutcutcodec.__main__
    return run_tests(light)


if __name__ == "__main__":
    sys.exit(main())
