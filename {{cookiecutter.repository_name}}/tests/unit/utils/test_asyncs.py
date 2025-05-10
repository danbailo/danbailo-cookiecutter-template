import asyncio
import time
from unittest.mock import MagicMock

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.asyncs import pool


def test_pool():
    sleep_time = 0.20
    task_amount = 10
    pool_size = 5
    logger = MagicMock()

    async def task():
        await asyncio.sleep(sleep_time)
        return True

    tasks = [task() for _ in range(task_amount)]

    async def run_test():
        start = time.perf_counter()

        async for result in pool(tasks, pool_size, logger):
            assert result

        duration = time.perf_counter() - start

        expected_duration = sleep_time * task_amount / pool_size
        assert expected_duration - 0.1 < duration < expected_duration + 0.1

    asyncio.run(run_test())
