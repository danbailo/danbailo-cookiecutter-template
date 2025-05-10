import asyncio
from typing import Any, Coroutine, TypeVar

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.factories.logger import Logger, LoggerFactory

T = TypeVar('T')


async def pool(
    tasks: list[Coroutine[Any, Any, T]], size=4, logger: Logger = LoggerFactory.new()
):
    """
    Executa a lista de funções assíncronas em paralelo, limitando a quantidade de funções
    executadas simultaneamente pelo parâmetro `size`, retornando um generator com os resultados.

    Caso alguma tarefa atire exceção, todas as tarefas restantes serão canceladas e a exceção será propagada.

    Exemplo:

    ```
    async def task(n: int) -> str:
        await asyncio.sleep(1)
        return str(n)


    async def main():
        tasks = [task(i) for i in range(10)]
        async for num in pool(tasks):
            print(num)


    asyncio.run(main())
    ```
    """
    pending = set(asyncio.create_task(task) for task in tasks[:size])
    tasks = tasks[size:]
    while pending:
        (done, pending) = await asyncio.wait(
            pending,
            return_when=asyncio.FIRST_COMPLETED,
        )
        while tasks and len(pending) < size:
            if len(tasks) % 10 == 0:
                logger.info(f'Tarefas restantes: {len(tasks)}')
            pending.add(asyncio.create_task(tasks.pop(0)))
        for task in done:
            yield task.result()
