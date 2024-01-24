# Copyright 2023-2025 Jeongmin Kang, jarvisNim @ GitHub
# See LICENSE for details.


from datetime import datetime, timedelta


from . import constant as cst


def find_30days_ago():
    _day30 = datetime.now() - timedelta(days=30)
    return _day30