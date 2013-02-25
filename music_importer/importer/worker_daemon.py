import signal, logging
import sys
import pickle
from time import sleep
from utils.daemon import Daemon
from importer import metaImport
from utils.rabbitmq import ack_message, get_message, MQType, close_connection

NEED_EXIT = False
INTERVAL = 0.2

_LOGGER = logging.getLogger("daemon")

def job_func(worker_name):
    queue_type = None
    if worker_name.startswith('vip'):
        queue_type = MQType.VIPQueue
    elif worker_name.startswith('quick'):
        queue_type = MQType.QuickQueue
    else:
        queue_type = MQType.NormalQueue

    method_frame, header_frame, body = get_message(queue_type)
    if method_frame == None or method_frame.NAME == "Basic.GetEmpty":
        return

    delivery_tag = method_frame.delivery_tag
    try:
        _LOGGER.info("Worker %s get message %s delivery-tag %i", worker_name, header_frame.content_type, delivery_tag)
        if metaImport(pickle.loads(body)):
            ack_message(delivery_tag, queue_type)
            _LOGGER.info("ack message with delivery tag: %s", delivery_tag)
    except Exception, e:
        try:
            ack_message(delivery_tag, queue_type)
            _LOGGER.info('Get exception: %s', str(meta))
            _LOGGER.exception('Error to process delivery-tag %i request data %s with exception: %s', delivery_tag, body, e)
        except Exception, e:
            _LOGGER.error('Get exception in worker_daemon exception handler: %s', e)

class WorkerDaemon(Daemon):
    def __init__(self, pidfile, work_name):
        Daemon.__init__(self, pidfile)
        self.name = work_name

    def run(self):
        signal.signal(signal.SIGTERM, SignalHandler)
        _LOGGER.info('Initializing worker %s..', self.name)
        while True:
            job_func(self.name)
            if NEED_EXIT:
                sys.exit()
            sleep(INTERVAL)

def SignalHandler(sig, id):
    if sig == signal.SIGTERM:
        _LOGGER.info('SIG %s received, stopping.', sig)
        global NEED_EXIT
        NEED_EXIT = True
