"""Entry point for the CloudLinux Python Selector (LiteSpeed lswsgi / Passenger).

The selector loads `application` from this file in the app root. It is copied
to the app root by deploy/deploy.sh along with wsgi.py and app/.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wsgi import app as application  # noqa: E402

__all__ = ["application"]
