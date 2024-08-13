# XXX provide proper typing for args by relying on boto3-stubs
import asyncio
from functools import partial

from boto3 import Session

from botoplier.sync.smart_query import _smart_query


# XXX typing
def smart_query(api, operation, *, session=None, executor=None, pagination=None, subtree=None, single=False, **kwargs):
    """See sync.smart_query() for full reference.

    In addition, this accepts an optional asyncio executor in which the query will be ran. We only really test this
    with a ThreadPoolExecutor. If you do not provide an executor, the default asyncio executor will be used.
    """  # noqa: D402
    session = session or Session()
    client = session.client(api, region_name=session.region_name)
    loop = asyncio.get_event_loop()
    closure = partial(_smart_query, client, operation, pagination=pagination, subtree=subtree, single=single, **kwargs)
    return loop.run_in_executor(executor, closure)
