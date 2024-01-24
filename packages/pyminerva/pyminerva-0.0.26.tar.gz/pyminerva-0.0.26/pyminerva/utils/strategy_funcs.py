# Copyright 2023-2025 Jeongmin Kang, jarvisNim @ GitHub
# See LICENSE for details.


from datetime import datetime, timedelta
from pytz import timezone

from . import constant as cst


def find_30days_ago():
    return (datetime.now() - timedelta(days=30)).dt.tz_localize('America/New_York').dt.tz_convert('UTC')