import asyncio
from .connection import Connection


__all__ = ("bridge_connections_unidirectional", "bridge_connections")


async def bridge_connections_unidirectional(a: Connection, b: Connection):
    task_closed = asyncio.create_task(b.writer.wait_closed())
    while True:
        # Wait for writer's close simultaneously with data to write, so that we can terminate the
        # read end immediately after the write end dies
        task_read = asyncio.create_task(a.reader.read(16384))
        done, pending = await asyncio.wait(
            [task_read, task_closed], return_when=asyncio.FIRST_COMPLETED
        )
        if task_read in done:
            try:
                buf = await task_read
                if not buf:
                    break
                b.writer.write(buf)
                # If an error happens during write, it will only be reported in drain
                await b.writer.drain()
            except ConnectionResetError:
                pass
        if task_closed in done:
            await task_closed
            break


async def bridge_connections(a: Connection, b: Connection):
    await asyncio.gather(bridge_connections_unidirectional(a, b), bridge_connections_unidirectional(b, a))
