import modal.client
import modal.io_streams
import typing
import typing_extensions

class _ContainerProcess:
    _process_id: typing.Union[str, None]
    _stdout: modal.io_streams._StreamReader
    _stderr: modal.io_streams._StreamReader
    _stdin: modal.io_streams._StreamWriter

    def __init__(self, process_id: str, client: modal.client._Client) -> None: ...
    @property
    def stdout(self) -> modal.io_streams._StreamReader: ...
    @property
    def stderr(self) -> modal.io_streams._StreamReader: ...
    @property
    def stdin(self) -> modal.io_streams._StreamWriter: ...
    async def attach(self, *, pty: bool): ...

class ContainerProcess:
    _process_id: typing.Union[str, None]
    _stdout: modal.io_streams.StreamReader
    _stderr: modal.io_streams.StreamReader
    _stdin: modal.io_streams.StreamWriter

    def __init__(self, process_id: str, client: modal.client.Client) -> None: ...
    @property
    def stdout(self) -> modal.io_streams.StreamReader: ...
    @property
    def stderr(self) -> modal.io_streams.StreamReader: ...
    @property
    def stdin(self) -> modal.io_streams.StreamWriter: ...

    class __attach_spec(typing_extensions.Protocol):
        def __call__(self, *, pty: bool): ...
        async def aio(self, *args, **kwargs): ...

    attach: __attach_spec
