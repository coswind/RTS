import pika, logging
from pika.adapters import BlockingConnection as Connection
from pika.reconnection_strategies import SimpleReconnectionStrategy
from music_importer.settings import MQ_CONF

_LOGGER = logging.getLogger('rabbitmq')

class MQType(object):
    NormalQueue = 1
    QuickQueue = 2
    VIPQueue = 3

connection = None
channel_dict = {
    MQType.NormalQueue : None,
    MQType.QuickQueue: None,
    MQType.VIPQueue: None,
}

exchanges = {
    MQType.NormalQueue : MQ_CONF["normal_exchange"],
    MQType.QuickQueue : MQ_CONF["quick_exchange"],
    MQType.VIPQueue : MQ_CONF["vip_exchange"],
}

queues = {
    MQType.NormalQueue : MQ_CONF["normal_queue"],
    MQType.QuickQueue : MQ_CONF["quick_queue"],
    MQType.VIPQueue : MQ_CONF["vip_queue"],
}

routings = {
    MQType.NormalQueue : MQ_CONF["normal_routing_key"],
    MQType.QuickQueue : MQ_CONF["quick_routing_key"],
    MQType.VIPQueue : MQ_CONF["vip_routing_key"],
}


def ensure_connection():
    global connection
    if connection:
        if not connection.is_open:
            close_connection()
        else:
            return connection

    # enable SimpleReconnectionStrategy.
    strategy = SimpleReconnectionStrategy()
    params = pika.ConnectionParameters(host = MQ_CONF["host"])
                                       # port = MQ_CONF["port"],
                                       # credentials=pika.PlainCredentials(MQ_CONF["user"],
                                       #                                   MQ_CONF["password"]),
                                       # virtual_host = MQ_CONF["vhost"])
    connection = Connection(parameters = params,
                            reconnection_strategy = strategy)
    return connection


def close_connection():
    global connection
    if not connection:
        return
    connection.close()
    connection = None


def open_channel():
    conn = ensure_connection()
    channel = conn.channel()
    channel.confirm_delivery()
    return channel


def on_channel_close(code, text):
    _LOGGER.error("channel closed with code: %s, text: %s.", code, text)
    for key in channel_dict.keys():
        channel_dict[key] = None


def ensure_channel(mq_type):
    k = mq_type
    if not channel_dict[k]:
        ch = open_channel()
        exchange_k = exchanges[k]
        queue_k = queues[k]
        routing_k = routings[k]
        ch.exchange_declare(exchange = exchange_k, type='direct', durable = True, auto_delete = False)
        ch.queue_declare(queue = queue_k, durable = True, exclusive = False, auto_delete = False)
        ch.queue_bind(queue = queue_k, exchange = exchange_k, routing_key = routing_k)
        #ch.basic_qos(prefetch_count = 1)
        ch.add_on_close_callback(on_channel_close)
        channel_dict[k] = ch

    return channel_dict[k]


def send_message(mq_type, message, properties):
    try:
        ch = ensure_channel(mq_type)
        k = mq_type
        exchange_k = exchanges[k]
        routing_k = routings[k]
        _LOGGER.info('asd')
        ch.basic_publish(exchange = exchange_k,
                         routing_key = routing_k,
                         body = message,
                         properties = properties)
    except Exception, e:
        _LOGGER.error("send_message %s failed. %s", mq_type, str(e))
        close_connection()

def get_message(mq_type):
    try:
        ch = ensure_channel(mq_type)
        k = mq_type
        queue_k = queues[k]
        return ch.basic_get(queue = queue_k, no_ack = False)
    except Exception, e:
        _LOGGER.exception(e)
        return None, None, None


def ack_message(delivery_tag, mq_type):
    try:
        ch = ensure_channel(mq_type)
        ch.basic_ack(delivery_tag = delivery_tag)
    except Exception, e:
        _LOGGER.exception(e)


def reject_message(delivery_tag, mq_type, re_queue=True):
    try:
        ch = ensure_channel(mq_type)
        ch.basic_reject(delivery_tag = delivery_tag, requeue=re_queue)
    except Exception, e:
        _LOGGER.exception(e)
