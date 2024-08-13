import asyncio
import socket
from collections.abc import AsyncGenerator, Generator, Iterator
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from typing import Protocol, Self, cast

from stompman.errors import ConnectionLostError
from stompman.frames import AnyClientFrame, AnyServerFrame
from stompman.serde import NEWLINE, FrameParser, dump_frame


@dataclass(kw_only=True)
class AbstractConnection(Protocol):
    @classmethod
    async def connect(
        cls, *, host: str, port: int, timeout: int, read_max_chunk_size: int, read_timeout: int
    ) -> Self | None: ...
    async def close(self) -> None: ...
    def write_heartbeat(self) -> None: ...
    async def write_frame(self, frame: AnyClientFrame) -> None: ...
    def read_frames(self) -> AsyncGenerator[AnyServerFrame, None]: ...


@contextmanager
def _reraise_connection_lost(*causes: type[Exception]) -> Generator[None, None, None]:
    try:
        yield
    except causes as exception:
        raise ConnectionLostError from exception


@dataclass(kw_only=True, slots=True)
class Connection(AbstractConnection):
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    read_max_chunk_size: int
    read_timeout: int

    @classmethod
    async def connect(
        cls, *, host: str, port: int, timeout: int, read_max_chunk_size: int, read_timeout: int
    ) -> Self | None:
        try:
            reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=timeout)
        except (TimeoutError, ConnectionError, socket.gaierror):
            return None
        else:
            return cls(reader=reader, writer=writer, read_max_chunk_size=read_max_chunk_size, read_timeout=read_timeout)

    async def close(self) -> None:
        self.writer.close()
        with suppress(ConnectionError):
            await self.writer.wait_closed()

    def write_heartbeat(self) -> None:
        with _reraise_connection_lost(RuntimeError):
            return self.writer.write(NEWLINE)

    async def write_frame(self, frame: AnyClientFrame) -> None:
        with _reraise_connection_lost(RuntimeError):
            self.writer.write(dump_frame(frame))
        with _reraise_connection_lost(ConnectionError):
            await self.writer.drain()

    async def _read_non_empty_bytes(self, max_chunk_size: int) -> bytes:
        while (chunk := await self.reader.read(max_chunk_size)) == b"":  # pragma: no cover (it defenitely happens)
            await asyncio.sleep(0)
        return chunk

    async def read_frames(self) -> AsyncGenerator[AnyServerFrame, None]:
        parser = FrameParser()

        while True:
            with _reraise_connection_lost(ConnectionError, TimeoutError):
                raw_frames = await asyncio.wait_for(
                    self._read_non_empty_bytes(self.read_max_chunk_size), timeout=self.read_timeout
                )

            for frame in cast(Iterator[AnyServerFrame], parser.parse_frames_from_chunk(raw_frames)):
                yield frame
