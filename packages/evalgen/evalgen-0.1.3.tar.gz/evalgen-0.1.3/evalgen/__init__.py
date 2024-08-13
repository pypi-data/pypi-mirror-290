r"""
"""
import os

VERSION = "0.1.3"

def _get_git_revision(path):
    revision_file = os.path.join(path, "refs", "heads", "master")
    if os.path.exists(revision_file):
        with open(revision_file) as fh:
            return fh.read().strip()[:7]


def get_revision():
    #
    #:returns: Revision number of this branch/checkout, if available. None if
    #    no revision number can be determined.
    #
    package_dir = os.path.dirname(__file__)
    checkout_dir = os.path.normpath(os.path.join(package_dir, os.pardir))
    path = os.path.join(checkout_dir, ".git")
    if os.path.exists(path):
        return _get_git_revision(path)

def get_version():
    """
    Revision number of this branch/checkout, if available. None if
    no revision number can be determined.
    """

    base = VERSION
    if __build__:
        base = "%s (%s)" % (base, __build__)
    return base

__build__ = get_revision()
__version__ = VERSION

from .access import *
from .specification import *
from .llm import *
from .lib import *
