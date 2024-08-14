from enum import IntEnum
from typing import Optional
import logging
from itertools import count


logger = logging.getLogger(__name__)


def _get_python_exceptions() -> list[type[BaseException]]:
    """Get Python built-in exceptions."""
    # See also https://docs.python.org/3/library/exceptions.html#exception-hierarchy.
    return [
        GeneratorExit,
        KeyboardInterrupt,
        SystemExit,
        Exception,
        ArithmeticError,
        FloatingPointError,
        OverflowError,
        ZeroDivisionError,
        AssertionError,
        AttributeError,
        BufferError,
        EOFError,
        EnvironmentError,
        IOError,
        OSError,
        BlockingIOError,
        ChildProcessError,
        ConnectionError,
        BrokenPipeError,
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        FileExistsError,
        FileNotFoundError,
        InterruptedError,
        IsADirectoryError,
        NotADirectoryError,
        PermissionError,
        ProcessLookupError,
        TimeoutError,
        ImportError,
        ModuleNotFoundError,
        LookupError,
        IndexError,
        KeyError,
        MemoryError,
        NameError,
        UnboundLocalError,
        ReferenceError,
        RuntimeError,
        NotImplementedError,
        RecursionError,
        StopAsyncIteration,
        StopIteration,
        SyntaxError,
        IndentationError,
        TabError,
        SystemError,
        TypeError,
        ValueError,
        UnicodeError,
        UnicodeDecodeError,
        UnicodeEncodeError,
        UnicodeTranslateError,
        StopIteration,
    ]


def _get_library_exceptions() -> list[type[Exception]]:
    """Get library exceptions."""
    return [
        # Client errors.
        ClientError,
        BadRequestError,
        NotFoundError,
        AuthenticationError,
        LengthRequiredError,
        # Server errors.
        ServerError,
        ServiceUnavailableError,
    ]


class Errors:
    """Error registry."""

    def __init__(self, error_classes: Optional[list[type[Exception]]] = None):
        """Initialize error registry."""
        self._classes_by_name: dict[type[Exception], int] = {}

        if error_classes:
            for error in error_classes:
                self.register(error)

    def register(self, error_class: type[Exception], name: Optional[str] = None):
        """Register an exception class."""
        if not name:
            name = error_class.__name__
        self._classes_by_name[name] = error_class

    def get(self, name: str) -> type[Exception]:
        """Get an exception class."""
        return self._classes_by_name[name]


def create_error_registry_with_built_in_exceptions() -> Errors:
    """Create an error registry with built-in exceptions.

    Creates an error registry with pre-registered Python and library exceptions.
    """
    built_in_exceptions = _get_library_exceptions() + _get_python_exceptions()
    return Errors(built_in_exceptions)


class ErrorRegistry:
    def __init__(self):
        self._code_by_error: dict[type[Exception], int] = {}
        self._error_by_code: dict[int, type[Exception]] = {}
        self._error_code_count = count(start=600)

    def _get_next_error_code(self) -> int:
        """Get next error code."""
        while True:
            status_code = next(self._error_code_count)
            if status_code not in self._error_by_code:
                return status_code

    def register_error(self, error_class: type[Exception], status_code: Optional[int] = None):
        """Register an error class."""
        if status_code is None:
            status_code = self._get_next_error_code()

        if not isinstance(status_code, int):
            raise TypeError(f"Error code must be an integer, not {type(status_code)}.")

        if status_code in self._error_by_code:
            raise ValueError("Error code already registered.")

        if not 600 <= status_code <= 699:
            raise ValueError("Error code must be between 600 and 699.")

        logger.debug("Registering %s with code %s.", error_class, status_code)

        self._code_by_error[error_class] = int(status_code)
        self._error_by_code[int(status_code)] = error_class

    def get_code(self, error_class: type[Exception]) -> int:
        """Get error code."""
        try:
            return self._code_by_error[error_class]
        except KeyError as error:
            raise ValueError(f"Error class not registered: {error}.")

    def get_error(self, code: int) -> type[Exception]:
        """Get error class."""
        try:
            return self._error_by_code[code]
        except KeyError:
            raise ValueError(f"Unknown error code: {code}")


_registry = ErrorRegistry()
_registry.register_error(error_class=Exception)
_registry.register_error(error_class=ArithmeticError)
_registry.register_error(error_class=FloatingPointError)
_registry.register_error(error_class=OverflowError)
_registry.register_error(error_class=ZeroDivisionError)
_registry.register_error(error_class=AssertionError)
_registry.register_error(error_class=AttributeError)
_registry.register_error(error_class=BufferError)
_registry.register_error(error_class=EOFError)
_registry.register_error(error_class=EnvironmentError)
_registry.register_error(error_class=IOError)
_registry.register_error(error_class=OSError)
_registry.register_error(error_class=ImportError)
_registry.register_error(error_class=LookupError)
_registry.register_error(error_class=IndexError)
_registry.register_error(error_class=KeyError)
_registry.register_error(error_class=MemoryError)
_registry.register_error(error_class=NameError)
_registry.register_error(error_class=UnboundLocalError)
_registry.register_error(error_class=ReferenceError)
_registry.register_error(error_class=RuntimeError)
_registry.register_error(error_class=NotImplementedError)
_registry.register_error(error_class=SyntaxError)
_registry.register_error(error_class=IndentationError)
_registry.register_error(error_class=TabError)
_registry.register_error(error_class=SystemError)
_registry.register_error(error_class=TypeError)
_registry.register_error(error_class=ValueError)
_registry.register_error(error_class=UnicodeError)
_registry.register_error(error_class=UnicodeDecodeError)
_registry.register_error(error_class=UnicodeEncodeError)
_registry.register_error(error_class=UnicodeTranslateError)
_registry.register_error(error_class=StopIteration)
_registry.register_error(error_class=GeneratorExit)
_registry.register_error(error_class=KeyboardInterrupt)
_registry.register_error(error_class=SystemExit)
_registry.register_error(error_class=SystemError)


def register_error(error_class: type[Exception], status_code: Optional[int] = None):
    """Register an error class."""
    _registry.register_error(error_class, status_code)


def get_error_code(error_class: type[Exception]) -> int:
    """Get error (status) code."""
    return _registry.get_code(error_class)


def get_error(status_code: int) -> type[Exception]:
    """Get error class."""
    return _registry.get_error(status_code)


class ConnectionTimeoutError(ConnectionError):
    """Raised when a connection fails due a timeout error."""


class ConnectTimeoutError(ConnectionTimeoutError):
    """Failed to establishing a connection in given time.

    Use set_timeout(timeout) to set a proper timeout. Note that connect_timeout
    and read_timeout can be defined as a tuple (connect_timeout, read_timeout).
    """


class ConnectionReadTimeoutError(ConnectionTimeoutError):
    """Failed to read data from a connection within given time out.

    Use set_timeout(timeout) to set a proper timeout. Note that connect_timeout
    and read_timeout can be defined as a tuple (connect_timeout, read_timeout).
    """


class ClientError(Exception):
    """4xx: Client error"""
    STATUS_CODE = 400

    @property
    def status_code(self) -> int:
        return self.STATUS_CODE


class BadRequestError(ClientError):
    """400: Bad request"""
    STATUS_CODE = 400


class AuthenticationError(ClientError):
    """401: Authentication error."""
    STATUS_CODE = 401


class NotFoundError(ClientError):
    """404: Not found error."""
    STATUS_CODE = 404


class ConflictError(ClientError):
    """409: Conflict error."""
    STATUS_CODE = 409


class LengthRequiredError(ClientError):
    """411: Content length required."""
    STATUS_CODE = 411



class ServerError(Exception):
    """5xx: Server error"""
    STATUS_CODE = 500

    @property
    def status_code(self) -> int:
        return self.STATUS_CODE


class ServiceUnavailableError(ServerError):
    """503: Service unavailable"""
    STATUS_CODE = 503


#class ApplicationError(Exception):
#    """6xx: Application error."""
