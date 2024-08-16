import io

from cleo.io.io import IO


class FakeCleoIoStringIO(io.StringIO, IO):
    pass
