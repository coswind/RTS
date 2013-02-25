import logging, traceback, sys
from thrift.transport import TTransport, TSocket
from thrift.protocol import TCompactProtocol

_LOGGER = logging.getLogger(__name__)

def exception_handled(logger = _LOGGER):
    def _decorator(func):
        def _view(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                exc_type, value, tb = sys.exc_info()
                formatted_tb = traceback.format_tb(tb)
                exception_message = 'An error occurred %s: %s traceback=%s' % (exc_type, value, formatted_tb)
                logger.error(exception_message)
        return _view
    return _decorator

def thrift_call(thrift_server,
    client_cls,
    result_cls=None,
    socket_cls=TSocket.TSocket,
    transport_cls=TTransport.TFramedTransport,
    protocol_cls=TCompactProtocol.TCompactProtocol
    ):
    """
    Decorator indicating call to thrift.

    Parameters:
        `thrift_server` : A tuple of (host, port) pair the indicates the thrift server.
        `client_cls` : The thrift client class.
        `result_cls` : Optional. A class or callable object which takes the thrift result as the argument,
                that converts thrift result to application applicable version. Default is None.
        `socket` : Optional. The socket class to use. Default is ``TSocket.TSocket``.
        `transport_cls` : Optional. The transport class to use. Default is ``TTransport.TFramedTransport``.
        `protocol_cls` : Optional. The protocol class to use. Default is ``TCompactProtocol.TCompactProtocol``.
    """
    def decorator(func):
        def inner(*args, **kwargs):
            host, port = thrift_server
            socket = socket_cls(host, port)
            transport = transport_cls(socket)
            result = None
            try:
                protocol = protocol_cls(transport)
                client = client_cls(protocol)
                transport.open()
                result = func(thrift_client=client, *args, **kwargs)
            except Exception:
                raise
            finally:
                transport.close()
            if result_cls and callable(result_cls):
                result = result_cls(result)
            return result
        inner.func_name = func.func_name
        return inner
    return decorator
