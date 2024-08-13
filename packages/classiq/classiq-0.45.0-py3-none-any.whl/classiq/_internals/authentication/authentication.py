from classiq._internals import async_utils
from classiq._internals.client import client


def authenticate(overwrite: bool = False) -> None:
    async_utils.run(authenticate_async(overwrite))


async def authenticate_async(overwrite: bool = False) -> None:
    """Async version of `register_device`"""
    await client().authenticate(overwrite)
