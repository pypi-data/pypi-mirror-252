import logging
from time import sleep

logger = logging.getLogger(__name__)


def rate_limit(headers) -> None:
    if headers["X-Rate-Limit-Remaining"] == 0:
        sleep(float(headers["X-Rate-Limit-Window"]))
    return None


def lm_pager(func, filters=None) -> list:
    items = list()
    offset, size = (
        0,
        1000,
    )  # LogicMonitor REST API v3 supports maximum size of 1000 records.
    data = (
        func(size=size, offset=offset, filter=filters)
        if filters
        else func(size=size, offset=offset)
    )
    items.extend(data[0].items)

    while data[0].total > offset + size:  # TODO async LM calls
        rate_limit(data[2])
        offset += size
        data = (
            func(size=size, offset=offset, filter=filters)
            if filters
            else func(size=size, offset=offset)
        )
        items.extend(data[0].items)

    return items
